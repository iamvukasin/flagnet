import glob
import os
import xml.etree.ElementTree as ET

import imageio
import ruamel.yaml as yaml

import config


def test_dataset_image_size():
    min_width, min_height = config.MIN_IMAGE_SIZE
    invalid_shaped_images = []

    for image_path in glob.glob(f'{config.DATASET_FOLDER}/*/*.jpg'):
        image = imageio.imread(image_path)
        width, height, channels = image.shape

        if width < min_width or min_height < min_height or channels != 3:
            invalid_shaped_images.append(image_path)

    invalid_shaped_images.sort()

    assert not invalid_shaped_images, f'These images have invalid shape (min size required: {width}x{height}):\n\t' \
                                      + '\n\t'.join(invalid_shaped_images)


def test_dataset_credits():
    images_not_found = []
    images_without_credits = []
    invalid_credits = []
    required_fields = ['author', 'download_url', 'downloader', 'filename', 'license', 'url']

    for country_folder in glob.glob(f'{config.DATASET_FOLDER}/*/'):
        images = {os.path.basename(path) for path in glob.glob(country_folder + '*.jpg')}
        images_with_credits = set()
        credits_file_path = country_folder + 'credits.yml'

        with open(credits_file_path) as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.Loader)

            if data['photos'] is not None:
                for photo_data in data['photos']:
                    if all([field in photo_data and photo_data[field] is not None for field in required_fields]):
                        images_with_credits.add(photo_data['filename'])
                    else:
                        invalid_credits.append(credits_file_path)
                        break

        images_not_found.extend([country_folder + image for image in images_with_credits.difference(images)])
        images_without_credits.extend([country_folder + image for image in images.difference(images_with_credits)])

    invalid_credits.sort()
    images_not_found.sort()
    images_without_credits.sort()

    assert not invalid_credits, f'These files have invalidly formatted credits:\n\t' \
                                + '\n\t'.join(invalid_credits)

    assert not images_not_found, f'These images have credits, but do not exist:\n\t' \
                                 + '\n\t'.join(images_not_found)

    assert not images_without_credits, f'These images do not have credits:\n\t' \
                                       + '\n\t'.join(images_without_credits)


class InvalidLabelFormat(Exception):
    def __init__(self, path: str):
        self.path = path


def test_dataset_labels():
    images_without_labels = []
    images_with_invalid_labels = []

    for image_path in glob.glob(f'{config.DATASET_FOLDER}/*/*.jpg'):
        folder_split = image_path.split('/')
        xml_file_path = image_path[:-3] + 'xml'
        folder_name = folder_split[-2]
        image_file_name = folder_split[-1]

        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            folder = root.find('folder')
            file_name = root.find('filename')

            if any([node is None for node in [folder, file_name]]):
                raise InvalidLabelFormat(image_path)

            if folder.text != folder_name or file_name.text != image_file_name:
                raise InvalidLabelFormat(image_path)

            for element in root.iter('object'):
                name = element.find('name')
                bounding_box = element.find('bndbox')

                if any([node is None for node in [name, bounding_box]]):
                    raise InvalidLabelFormat(image_path)

                if name.text != folder_name:
                    raise InvalidLabelFormat(image_path)

                xmin = bounding_box.find('xmin')
                xmax = bounding_box.find('xmax')
                ymin = bounding_box.find('ymin')
                ymax = bounding_box.find('ymax')

                if any([node is None for node in [xmin, xmax, ymin, ymax]]):
                    raise InvalidLabelFormat(image_path)
        except IOError:
            images_without_labels.append(image_path)
        except InvalidLabelFormat as err:
            images_with_invalid_labels.append(err.path)

    images_without_labels.sort()
    images_with_invalid_labels.sort()

    assert not images_without_labels, f'These images do not have labels:\n\t' \
                                      + '\n\t'.join(images_without_labels)

    assert not images_with_invalid_labels, f'These images have invalidly formatted label files:\n\t' \
                                           + '\n\t'.join(images_with_invalid_labels)
