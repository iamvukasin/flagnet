import os

PROJECT_ROOT = os.path.dirname(__file__)

DATASET_FOLDER = os.path.join(PROJECT_ROOT, 'dataset')
CACHE_FOLDER = os.path.join(PROJECT_ROOT, '.cache')

# minimum size of images in the dataset
MIN_IMAGE_SIZE = 416, 416

# size of generated images from Flagwaver website
SCREENSHOT_IMAGE_SIZE = 800, 600

# number of parallel workers when downloading the dataset
NUM_DOWNLOAD_WORKERS = 8
