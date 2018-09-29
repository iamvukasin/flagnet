import glob
import re

import jinja2
import ruamel.yaml as yaml

import config

_CREDITS_TEMPLATE = """\
# {{country.flag}} Photo credits for flags of {{country.name}} ({{country.code}})
{% if photos is iterable -%}
    {% for photo in photos %}
  - `{{photo.filename}}` by {{photo.author}}, licensed under the {{photo.license}} license ([source]({{photo.url}}))
    {%- endfor %}
{% else %}
No photos added
{% endif %}
"""


def _create_markdown_from_yaml(yaml_file_path: str):
    """
    Creates photo credits file in Markdown from a YAML file, based on
    predefined template.

    :param yaml_file_path: a file path of a YAML file which is used
    as a data input source
    """

    markdown_file_path = re.sub(r'\.ya?ml', '.md', yaml_file_path)

    with open(yaml_file_path) as yaml_file, open(markdown_file_path, 'w') as markdown_file:
        data = yaml.load(yaml_file, Loader=yaml.Loader)
        template = jinja2.Template(_CREDITS_TEMPLATE)
        markdown_file.write(template.render(data))


if __name__ == '__main__':
    for country_folder in glob.glob(f'../{config.DATASET_FOLDER}/*/'):
        _create_markdown_from_yaml(f'{country_folder}credits.yml')
