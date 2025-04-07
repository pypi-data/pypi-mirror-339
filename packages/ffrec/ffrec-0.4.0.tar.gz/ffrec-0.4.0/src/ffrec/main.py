# src/ffrec/main.py

import asyncio
import logging
import os
from datetime import datetime
from ffrec.lib.parse_args import parse_arguments
from ffrec.lib.record_screen import record_screen


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_current_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")


async def main():
    args = parse_arguments()

    if args.debug:
        log_level = logging.DEBUG
    elif args.verbose > 0:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    if args.timestamp:
        timestamp = get_current_timestamp()
        output_file = f"{args.prefix}-{timestamp}.mp4"
    else:
        output_file = f"{args.prefix}.mp4"
    output_path = os.path.join(args.dir, output_file)

    try:
        await record_screen(
            output_path,
            audio_codec=args.audio_codec,
            audio_input=args.audio_input,
            video_codec=args.video_codec,
            audio_channels=args.audio_channels,
            input_source="x11grab",
            loop=args.loop,
            record_mouse=args.mouse,
            overwrite=args.overwrite,
            size=args.size,
            framerate=args.framerate,
            duration=args.time,
        )
        logging.info(f"Screen recording saved to {output_path}")
    except Exception as e:
        logging.error("Failed to complete screen recording: %s", e)


def main_wrapper():
    asyncio.run(main())


if __name__ == "__main__":
    main_wrapper()
