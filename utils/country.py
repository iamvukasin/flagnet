import json
import os
from collections import namedtuple
from typing import List

import requests
from urllib3.exceptions import MaxRetryError

import config

_WIKIDATA_QUERY_ENDPOINT_URL = 'https://query.wikidata.org/sparql'
_COUNTRIES_CACHE_FILE = 'countries.json'
_WIKIDATA_COUNTRIES_QUERY = """\
SELECT ?countryLabel ?code (?shortName AS ?flag) ?flagImage
WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }

  ?country wdt:P31 wd:Q3624078;          # sovereign states only
           wdt:P297 ?code;               # ISO 3166-1 alpha-2 two-letter country code
           wdt:P41 ?flagImage;           # URL to SVG flag image from WikiCommons
           wdt:P1813 ?shortName;         # short names for every country, including Unicode country flag emojis
           p:P1813 ?shortNameStatement.

  # keep countries with flag emojis only
  ?shortNameStatement pq:P31 ?type.
  FILTER(LANG(?shortName) = "zxx" && ?type = wd:Q28840786).
  FILTER(regex(str(?shortName), "[\\\\x{0001F1E6}-\\\\x{0001F1FF}]{2}")).

  # keep countries which are currently members of the United Nations
  ?country p:P463 ?statement.
  ?statement ps:P463 ?organization.
  FILTER (?organization = wd:Q1065)
  FILTER NOT EXISTS { ?statement pq:P582 ?endDate }
}
ORDER BY ?code
"""

Country = namedtuple('Country', ['code', 'name', 'flag', 'flag_image'])


class NoCountriesException(Exception):
    """
    Simple exception class to indicate connection issues or no response from
    the Wikidata endpoint.
    """
    pass


def load_countries(forced: bool = False) -> List[Country]:
    """
    Returns a list of countries from the cache folder (if it exists) or
    requests the newest list of countries from Wikidata, creates a cached copy
    and returns the list. It is useful because the list of countries rarely
    changes and there is no need to get it from Wikidata.

    :param forced: an indicator to skip the cached countries and to load
    the newest list of countries from Wikidata
    :return: a list of countries with two-letter country code, name, flag
    emoji, and flag image URL from WikiCommons for every country
    """

    cache_folder = f'../{config.CACHE_FOLDER}'
    cache_file_path = f'{cache_folder}/{_COUNTRIES_CACHE_FILE}'

    # create cache folder or skip if it exists
    os.makedirs(cache_folder, exist_ok=True)

    # load the list of countries from a JSON file located in the cache folder
    if not forced and os.path.isfile(cache_file_path):
        with open(cache_file_path) as file:
            data = json.load(file)
            return [Country(**country) for country in data['countries']]

    no_connection = False
    r = None

    try:
        r = requests.get(_WIKIDATA_QUERY_ENDPOINT_URL, params={
            'format': 'json',
            'query': _WIKIDATA_COUNTRIES_QUERY
        })
    except MaxRetryError:
        no_connection = True

    assert r is not None

    if no_connection or r.status_code != 200:
        raise NoCountriesException('Cannot load countries from Wikidata')

    data = r.json()
    countries = []

    # parse Wikidata endpoint result
    for result in data['results']['bindings']:
        country_code = result['code']['value']
        country_name = result['countryLabel']['value']
        country_flag = result['flag']['value']
        country_flag_image = result['flagImage']['value']
        country = Country(code=country_code,
                          name=country_name,
                          flag=country_flag,
                          flag_image=country_flag_image)
        countries.append(country)

    # save the country list as a JSON file in the cache folder
    with open(cache_file_path, 'w') as file:
        countries_dict = {
            'countries': [country._asdict() for country in countries]
        }
        json.dump(countries_dict, file)

    return countries


def _create_country_folders(countries: List[Country]):
    """
    Creates country folders inside the dataset folder. Every country folder
    has photos of flags, and a YAML/Markdown file with image credits for
    every photo.

    :param countries: a list of countries loaded from the cache folder or
    Wikidata
    """

    for country in countries:
        folder_path = f'../{config.DATASET_FOLDER}/{country.code.lower()}'
        os.makedirs(folder_path, exist_ok=True)

        with open(f'{folder_path}/credits.yml', 'w') as file:
            file.write(('country:\n'
                        f'  name: {country.name}\n'
                        f'  code: {country.code}\n'
                        f'  flag: {country.flag}\n'
                        'photos:\n'))


def _create_label_map(countries: List[Country]):
    """
    Creates a label map for countries in protocol buffers format.

    :param countries: a list of countries loaded from the cache folder or
    Wikidata
    """

    with open(f'../{config.DATASET_FOLDER}/countries_label_map.pbtxt', 'w') as file:
        for id_, country in enumerate(countries):
            file.write(('item {\n'
                        f'  id: {id_ + 1}\n'
                        f'  name: "{country.code.lower()}"\n'
                        f'  display_name: "{country.name}"\n'
                        '}\n'))


if __name__ == '__main__':
    all_countries = load_countries()
    _create_country_folders(all_countries)
    _create_label_map(all_countries)
