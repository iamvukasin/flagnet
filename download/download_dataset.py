import glob

import ruamel.yaml as yaml

import config
from download.url_image_downloader import UrlImageDownloader

_DOWNLOADERS = {downloader.type: downloader for downloader in (UrlImageDownloader,)}

if __name__ == '__main__':
    for credits in glob.glob(f'{config.DATASET_FOLDER}/*/credits.yml'):
        # read all photos for single class
        with open(credits) as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.Loader)

        # download all photos
        for photo_data in data['photos']:
            download_url = photo_data['download_url']
            path = credits.replace('credits.yml', photo_data['filename'])
            downloader = _DOWNLOADERS[photo_data['downloader']](download_url, path)
            downloader.download()
