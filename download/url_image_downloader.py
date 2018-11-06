import requests

from download.image_dowloader import ImageDownloader


class UrlImageDownloader(ImageDownloader):
    """
    An image downloader from URL.
    """

    type = 'url_image'

    def __init__(self, url: str, path: str):
        super().__init__(url, path)

    def _download_from_url(self):
        with open(self.path, 'wb') as image:
            image.write(requests.get(self.url).content)
