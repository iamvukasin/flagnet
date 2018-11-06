import abc
import os


class ImageDownloader(abc.ABC):
    """
    An abstract image downloader.
    """

    def __init__(self, url: str, path: str):
        self.url = url
        self.path = path

    def download(self):
        if not os.path.isfile(self.path):
            self._download_from_url()

    @abc.abstractmethod
    def _download_from_url(self):
        pass

    @property
    def type(self):
        raise NotImplementedError
