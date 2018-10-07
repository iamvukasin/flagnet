import hashlib
import io
import re
import time
import urllib.parse

import ruamel.yaml as yaml
from PIL import Image
from selenium import webdriver

import config
from utils.country import load_countries

_FLAGWAVER_URL = 'https://iamvukasin.github.com/flagwaver'
_SCREENSHOTS_AUTHOR = 'Vukašin Manojlović'
_SCREENSHOTS_LICENSE = 'CC0 Public Domain'


def _take_screenshot(url: str, screenshot_path: str, timeout: float = 0.0):
    """
    Takes a screenshot of a page located at the given URL and saves it onto
    the given path. Optionally, it can wait some time after page loads, and
    then takes a screenshot.

    :param url: a page URL which will be saved as a screenshot
    :param screenshot_path: a file path where the taken screenshot will be
    saved (has to include .jpg extension)
    :param timeout: time in seconds to wait between loading the page and
    taking a screenshot
    """

    if screenshot_path[-4:] != '.jpg':
        raise ValueError('Screenshot has to be saved as a JPG file')

    # hide all Chrome UI elements (aka headless mode) and make page content
    # fill the window - this will make screenshot to be the same size as the
    # window (see: driver.set_window_size)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # set Google Chrome as Selenium driver
    # note: ChromeDriver has to be properly installed to make this work
    driver = 'chromedriver'
    driver = webdriver.Chrome(driver, options=options)

    driver.get(url)
    driver.set_window_size(*config.IMAGE_SIZE)

    # wait before taking a screenshot
    time.sleep(timeout)

    # save the screenshot as JPEG
    png_screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(io.BytesIO(png_screenshot)).convert('RGB')
    screenshot.save(screenshot_path, format='JPEG', quality=100)

    driver.quit()


def convert_wikicommons_url_to_png_url(url: str, image_width: int = 1000) -> str:
    """
    Generates a URL to a PNG version of the SVG file from Wikimedia Commons
    file URL.

    :param url: a URL to the SVG file from Wikimedia Commons
    :param image_width: a width of the PNG image
    :return: a URL to the PNG version of the given Wikimedia Commons URL
    """

    if image_width <= 0:
        raise ValueError(f'Image width has to be a positive number, passed {image_width}')

    match = re.match(r'https?://commons\.wikimedia\.org/wiki/(?:Special:FilePath/|File:)(.+)', url)

    if not match or url[-4:] != '.svg':
        raise ValueError(f'Invalid Wikimedia Commons URL passed: {url}')

    file_name = match.group(1)
    file_name = urllib.parse.unquote(file_name).replace(' ', '_')
    md5_hash = hashlib.md5(file_name.encode('utf-8')).hexdigest()

    return (f'https://upload.wikimedia.org/wikipedia/commons/thumb/'
            f'{md5_hash[0]}/{md5_hash[:2]}/{file_name}/{image_width}px-{file_name}.png')


if __name__ == '__main__':
    countries = load_countries()
    wind_directions = [90, 270]
    flag_top_edges = ['top', 'left', 'right']

    for country in countries:
        print(f'Taking screenshots of flags of {country.name}')
        country_code = country.code.lower()
        i = 0

        with open(f'../{config.DATASET_FOLDER}/{country_code}/credits.yml', 'r') as credits_file:
            credits_data = yaml.load(credits_file, Loader=yaml.Loader)
            credits_data.pop('photos', None)
            credits_data['photos'] = []

        with open(f'../{config.DATASET_FOLDER}/{country_code}/credits.yml', 'w') as credits_file:
            for direction in wind_directions:
                for edge in flag_top_edges:
                    image_source = convert_wikicommons_url_to_png_url(country.flag_image)
                    flagwaver_url = (f'{_FLAGWAVER_URL}/#?hideui=true'
                                     f'&direction={direction}&topedge={edge}&src={image_source}&windtype=fixed')
                    file_name = f'{country_code}_{i:05}.jpg'
                    screenshot_path = f'../{config.DATASET_FOLDER}/{country_code}/{file_name}'

                    # print generated flagwaver URL
                    print(flagwaver_url)

                    _take_screenshot(url=flagwaver_url,
                                     screenshot_path=screenshot_path,
                                     timeout=6)

                    # add credits for generated screenshots
                    credits_data['photos'].append({
                        'author': _SCREENSHOTS_AUTHOR,
                        'filename': file_name,
                        'license': _SCREENSHOTS_LICENSE,
                        'url': _FLAGWAVER_URL
                    })

                    i += 1

            # write modified credits back
            yaml.dump(credits_data, credits_file, default_flow_style=False, allow_unicode=True)
