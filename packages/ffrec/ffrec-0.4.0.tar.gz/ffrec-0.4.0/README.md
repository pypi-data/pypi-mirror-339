# ffrec
ffrec records the screen, using Python.

* https://spacecruft.org/deepcrayon/ffrec
* https://pypi.org/project/ffrec/

# Installation
Thusly, suit to taste:

```
python -m venv venv
source venv/bin/activate
pip install -U setuptools pip wheel
pip install ffrec
```

# Help
Command line options:

```
$ ffrec --help
usage: ffrec [-h] [-a AUDIO_CODEC] [-A AUDIO_INPUT] [-c VIDEO_CODEC] [-D] [-C AUDIO_CHANNELS] [-d DIR] [-l] [-m] [-o] [-p PREFIX] [-r FRAMERATE] [-s SIZE] [-t TIME] [-T | -N] [-v] [-V]

Record screen and save to mp4

options:
  -h, --help            show this help message and exit
  -a AUDIO_CODEC, --audio-codec AUDIO_CODEC
                        Audio codec to use (default: aac)
  -A AUDIO_INPUT, --audio-input AUDIO_INPUT
                        Audio input source (default: pulse)
  -c VIDEO_CODEC, --video-codec VIDEO_CODEC
                        Video codec to use (default: hevc_nvenc)
  -D, --debug           Debugging
  -C AUDIO_CHANNELS, --audio-channels AUDIO_CHANNELS
                        Number of audio channels (default: 2)
  -d DIR, --dir DIR     Directory to save the output video file
  -l, --loop            Loop input until stream is terminated manually
  -m, --mouse           Record the mouse cursor (default false)
  -o, --overwrite       Overwrite existing files (default: true)
  -p PREFIX, --prefix PREFIX
                        Prefix for the output video file name
  -r FRAMERATE, --framerate FRAMERATE
                        Framerate for recording (default: 30)
  -s SIZE, --size SIZE  Video size (default: 1920x1080)
  -t TIME, --time TIME  Length of recording in HH:MM:SS format (default: 00:01:00)
  -T, --timestamp       Add timestamp to filename (default)
  -N, --no-timestamp    Do not add timestamp to filename
  -v, --verbose         Increase output verbosity
  -V, --version         Show version
```

# License
Apache 2.0 or Creative Commons CC by SA 4.0 International.
You may use this code, files, and text under either license.

Unofficial project, not related to upstream projects.

Upstream sources under their respective copyrights.

*Copyright &copy; 2025 Jeff Moe.*
