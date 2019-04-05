# Flagnet

[![Build Status](https://travis-ci.com/iamvukasin/flagnet.svg?branch=master)](https://travis-ci.com/iamvukasin/flagnet)
[![License MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Flagnet is a neural network for detecting country flags in photos. The detection is backed up by our very own dataset –
the collection of photos of flags for 193 United Nations member countries.

## Table of contents

  * [Getting started](#getting-started)
     * [Configuration](#configuration)
     * [Dataset](#dataset)
  * [Contributing](#contributing)
  * [License](#license)

## Getting started

Flagnet is built in Python 3. Before cloning the project, make sure that you have downloaded and installed
[Python](https://www.python.org/downloads/) and
[Pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv).

After downloading Python and Pipenv, you have to download all dependencies via Pipenv:

```bash
$ pipenv install
```

Now you're ready for the project!

### Configuration

All project configuration is controlled from a single place – the `config.py` file. Currently you can change these
parameters:

```python
MIN_IMAGE_SIZE = 416, 416         # minimum size of images in the dataset
SCREENSHOT_IMAGE_SIZE = 800, 600  # size of generated images from Flagwaver website
```

### Dataset

The images which are part of the dataset are stored in the `dataset` folder and organized into the folders by country
ISO 3166-1 alpha-2 codes. Inside every folder, there is a `credits.yml` (and its visual Markdown representation
`credits.md`) which contains a list of images with its author name, license and download URL. To download the dataset,
position yourself in the root of the project and run the downloader:

```bash
$ python -m download.download_dataset
```

## Contributing

Pull requests are welcome for both the dataset and the neural network.

## License

Flagnet is released under the [MIT license](LICENSE).