# vidtoolz-add-text

[![PyPI](https://img.shields.io/pypi/v/vidtoolz-add-text.svg)](https://pypi.org/project/vidtoolz-add-text/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-add-text?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-add-text/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-add-text/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-add-text/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-add-text/blob/main/LICENSE)

Add text to a video file using FFmpeg (default) or MoviePy

![Demo](https://raw.githubusercontent.com/sukhbinder/vidtoolz-add-text/refs/heads/main/demo.png)

## Installation

First install [vidtoolz](https://github.com/sukhbinder/vidtoolz).

```bash
pip install vidtoolz
```

Then install this plugin in the same environment as your vidtoolz application.

```bash
vidtoolz install vidtoolz-add-text
```

**Note:** FFmpeg is required. The plugin will automatically try to use FFmpeg from your system path, or fall back to [static-ffmpeg](https://pypi.org/project/static-ffmpeg/) if available.

## Usage

type ``vid addtext --help`` to get help

```bash
usage: vid addtext [-h] [-t TEXT] [-mt MULTI_TEXT] [-o OUTPUT]
                   [-p {top-left,top-right,bottom-left,bottom-right,center,bottom}]
                   [-st START_TIME] [-et END_TIME] [-f FONTSIZE]
                   [-pad PADDING] [-d DURATION] [--use-moviepy] [-x X] [-y Y]
                   main_video

Add text to a video file

positional arguments:
  main_video            Path to the main video file.

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Text to write
  -mt MULTI_TEXT, --multi-text MULTI_TEXT
                        Multi-text in format "text,start,duration". Can be
                        used multiple times. ex "hello,1:20,10"
  -o OUTPUT, --output OUTPUT
                        Output video file name (default: None)
  -p {top-left,top-right,bottom-left,bottom-right,center,bottom}, --position {top-left,top-right,bottom-left,bottom-right,center,bottom}
                        Position of the text (default: bottom)
  -st START_TIME, --start-time START_TIME
                        Start time when text should appear (supports formats like "1:20" or seconds) (default: 0)
  -et END_TIME, --end-time END_TIME
                        End time when text should disappear (supports formats like "1:20" or seconds) (default: None)
  -f FONTSIZE, --fontsize FONTSIZE
                        Fontsize (default: 70)
  -pad PADDING, --padding PADDING
                        Padding (default: 50)
  -d DURATION, --duration DURATION
                        Duration in seconds (default: 4)
  --use-moviepy         If provided, use MoviePy instead of FFmpeg
  -x X, --x X           X position of the overlay (can be number or FFmpeg expression, e.g., 'main_w-text_w')
  -y Y, --y Y           Y position of the overlay (can be number or FFmpeg expression, e.g., 'main_h-text_h')


```

### Examples

Add text at the bottom of the video (default position):
```bash
vid addtext -t "Hello World" input.mp4
```

Add text at a specific position with custom timing:
```bash
vid addtext -t "Hello World" -p top-right -st 10 -et 20 input.mp4
```

Add text with time format (minutes:seconds):
```bash
vid addtext -t "Hello World" -st 0:30 -et 1:15 input.mp4
```

Add multiple text overlays:
```bash
vid addtext -mt "Hello,0:10,5" -mt "World,0:20,5" input.mp4
```

Use MoviePy instead of FFmpeg:
```bash
vid addtext -t "Hello World" --use-moviepy input.mp4
```

Custom positioning with FFmpeg expressions:
```bash
vid addtext -t "Hello World" -x 100 -y 100 input.mp4
```

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
