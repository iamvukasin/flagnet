import glob
import config
import imageio


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
