# vidtoolz-add-text

[![PyPI](https://img.shields.io/pypi/v/vidtoolz-add-text.svg)](https://pypi.org/project/vidtoolz-add-text/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-add-text?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-add-text/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-add-text/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-add-text/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-add-text/blob/main/LICENSE)

Add text to a video file

## Installation

First install [vidtoolz](https://github.com/sukhbinder/vidtoolz).

```bash
pip install vidtoolz
```

Then install this plugin in the same environment as your vidtoolz application.

```bash
vidtoolz install vidtoolz-add-text
```
## Usage

type ``vid addtext --help`` to get help



## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd vidtoolz-add-text
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
