import glob
from collections import namedtuple
from multiprocessing.pool import ThreadPool

import ruamel.yaml as yaml

import config
from download.url_image_downloader import UrlImageDownloader

PhotoItem = namedtuple('PhotoItem', ['downloader', 'download_url', 'path'])

DOWNLOADERS = {downloader.type: downloader for downloader in (UrlImageDownloader,)}


def _download_single_photo(item: PhotoItem):
    """
    Downloads a single photo with the given downloader, the URL to download
    from and the local path where to store the downloaded photo.

    :param item: a tuple which contains downloader name, download URL and
    local path
    """

    downloader = DOWNLOADERS[item.downloader](item.download_url, item.path)
    downloader.download()


if __name__ == '__main__':
    photo_items = []

    for credits in glob.glob(f'{config.DATASET_FOLDER}/*/credits.yml'):
        # read all photos for a single country
        with open(credits) as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.Loader)

        for photo_data in data['photos']:
            downloader_type = photo_data['downloader']
            download_url = photo_data['download_url']
            path = credits.replace('credits.yml', photo_data['filename'])

            item = PhotoItem(
                downloader=downloader_type,
                download_url=download_url,
                path=path
            )
            photo_items.append(item)

    # download photos in parallel
    results = ThreadPool(config.NUM_DOWNLOAD_WORKERS).imap_unordered(_download_single_photo, photo_items)

    # wait all downloads to finish
    for _ in results:
        pass
