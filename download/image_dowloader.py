import abc
import os


class ImageDownloader(abc.ABC):
    """
    An abstract image downloader.
    """

    def __init__(self, url: str, path: str, forced: bool = False):
        self.url = url
        self.path = path
        self.forced = forced

    def download(self):
        if self.forced or not os.path.isfile(self.path):
            print(f'Downloading {self.path}...')
            self._download_from_url()
        else:
            print(f'Download of {self.path} is skipped')

    @abc.abstractmethod
    def _download_from_url(self):
        pass

    @property
    def type(self):
        raise NotImplementedError
