import os
import hashlib

from download.url_image_downloader import UrlImageDownloader


def test_download_image_from_url():
    url = ('https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/RacingFlagsJune2007.jpg/575px-'
           'RacingFlagsJune2007.jpg')
    image_path = 'test.jpg'

    # download the image
    downloader = UrlImageDownloader(url, image_path)
    downloader.download()

    md5 = hashlib.md5()

    # calculate md5 hash of the downloaded image
    with open(image_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5.update(chunk)

    assert os.path.isfile(image_path)
    assert md5.hexdigest() == '82a8ebf6719a24b52dec3fa6856d4870'

    # remove the downloaded image
    os.remove(image_path)
