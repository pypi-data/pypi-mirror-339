# src/ffrec/lib/parse_args.py

import argparse
import os
from ffrec._version import __version__


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record screen and save to mp4")

    parser.add_argument(
        "-a",
        "--audio-codec",
        help="Audio codec to use (default: aac)",
        default="aac",
    )

    parser.add_argument(
        "-A",
        "--audio-input",
        help="Audio input source (default: pulse)",
        default="pulse",
    )

    parser.add_argument(
        "-c",
        "--video-codec",
        help="Video codec to use (default: hevc_nvenc)",
        default="hevc_nvenc",
    )

    parser.add_argument(
        "-D",
        "--debug",
        help="Debugging",
        action="store_true",
    )

    parser.add_argument(
        "-C",
        "--audio-channels",
        help="Number of audio channels (default: 2)",
        type=int,
        default=2,
    )

    parser.add_argument(
        "-d",
        "--dir",
        help="Directory to save the output video file",
        default=os.getcwd(),
    )

    # parser.add_argument(
    #     "-i",
    #     "--input",
    #     help="Input source for recording (default: x11grab)",
    #     choices=["x11grab", "wayland", "kmsgrab"],
    #     default="x11grab",
    # )

    parser.add_argument(
        "-l",
        "--loop",
        help="Loop input until stream is terminated manually",
        action="store_true",
    )

    parser.add_argument(
        "-m",
        "--mouse",
        help="Record the mouse cursor (default false)",
        action="store_true",
    )

    parser.add_argument(
        "-o",
        "--overwrite",
        help="Overwrite existing files (default: true)",
        action="store_true",
        default=True,
    )

    parser.add_argument(
        "-p",
        "--prefix",
        help="Prefix for the output video file name",
        default="video",
    )

    parser.add_argument(
        "-r",
        "--framerate",
        help="Framerate for recording (default: 30)",
        type=int,
        default=30,
    )

    parser.add_argument(
        "-s",
        "--size",
        help="Video size (default: 1920x1080)",
        default="1920x1080",
    )

    parser.add_argument(
        "-t",
        "--time",
        help="Length of recording in HH:MM:SS format (default: 00:01:00)",
        default="00:01:00",
    )

    timestamp_group = parser.add_mutually_exclusive_group(required=False)
    timestamp_group.add_argument(
        "-T",
        "--timestamp",
        help="Add timestamp to filename (default)",
        action="store_true",
        default=True,
    )
    timestamp_group.add_argument(
        "-N",
        "--no-timestamp",
        help="Do not add timestamp to filename",
        action="store_false",
        dest="timestamp",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="Increase output verbosity",
        action="count",
        default=0,
    )

    parser.add_argument(
        "-V",
        "--version",
        help="Show version",
        action="version",
        version=f"{__version__}",
    )

    args = parser.parse_args()

    return args
