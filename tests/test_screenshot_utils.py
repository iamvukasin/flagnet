import urllib.parse

from utils.screenshot import convert_wikicommons_url_to_png_url


def test_wikimedia_commons_url_conversion():
    image_width = 1000
    commons_urls = [
        'https://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Serbia.svg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20France.svg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Russia.svg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20People\'s%20Republic%20of%20China.svg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20United%20Kingdom.svg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20United%20States.svg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Venezuela.svg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20New%20Zealand.svg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Kenya.svg',
        'https://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Brazil.svg'
    ]
    png_version_urls = [
        (f'https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Flag_of_Serbia.svg/{image_width}px-Flag_of_Serbia'
         '.svg.png'),
        (f'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Flag_of_France.svg/{image_width}px-Flag_of_France'
         '.svg.png'),
        (f'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Russia.svg/{image_width}px-Flag_of_Russia'
         '.svg.png'),
        ('https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Flag_of_the_People%27s_Republic_of_China.svg/'
         f'{image_width}px-Flag_of_the_People%27s_Republic_of_China.svg.png'),
        (f'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Flag_of_the_United_Kingdom.svg/{image_width}px'
         '-Flag_of_the_United_Kingdom.svg.png'),
        (f'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Flag_of_the_United_States.svg/{image_width}px-Flag'
         '_of_the_United_States.svg.png'),
        (f'https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Flag_of_Venezuela.svg/{image_width}px-Flag_of'
         '_Venezuela.svg.png'),
        (f'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Flag_of_New_Zealand.svg/{image_width}px-Flag_of'
         '_New_Zealand.svg.png'),
        (f'https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/{image_width}px-Flag_of_Kenya'
         '.svg.png'),
        (f'https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/{image_width}px-Flag_of_Brazil'
         '.svg.png')
    ]

    for commons_url, png_url in zip(commons_urls, png_version_urls):
        converted_url = convert_wikicommons_url_to_png_url(commons_url, image_width=image_width)
        assert urllib.parse.unquote(converted_url) == urllib.parse.unquote(png_url)
