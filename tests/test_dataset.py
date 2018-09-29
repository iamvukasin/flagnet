import glob
import os

import imageio
import ruamel.yaml as yaml

import config


def test_dataset_image_size():
    width, height = config.IMAGE_SIZE
    valid_image_shape = (height, width, 3)  # RGB images only

    invalid_shaped_images = []

    for image_path in glob.glob(f'{config.DATASET_FOLDER}/*/*.jpg'):
        image = imageio.imread(image_path)

        if image.shape != valid_image_shape:
            invalid_shaped_images.append(image_path)

    assert not invalid_shaped_images, f'These images have invalid shape (required {width}x{height}):\n\t' \
                                      + "\n\t".join(invalid_shaped_images)


def test_dataset_credits():
    images_not_found = []
    images_without_credits = []
    invalid_credits = []
    required_fields = ['author', 'filename', 'license', 'url']

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

    assert not invalid_credits, f'These files have invalidly formatted credits:\n\t' \
                                + "\n\t".join(invalid_credits)

    assert not images_not_found, f'These images have credits, but do not exist:\n\t' \
                                 + "\n\t".join(images_not_found)

    assert not images_without_credits, f'These images do not have credits:\n\t' \
                                       + "\n\t".join(images_without_credits)
