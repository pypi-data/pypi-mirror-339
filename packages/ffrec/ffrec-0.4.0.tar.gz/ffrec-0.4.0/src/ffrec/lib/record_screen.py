import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from ffmpeg import FFmpeg, Progress


def run_ffmpeg_process(ffmpeg_process):
    try:

        @ffmpeg_process.on("progress")
        def on_progress(progress: Progress):
            logging.debug("Progress: %s", progress)

        ffmpeg_process.execute()
        logging.info("FFmpeg process completed successfully")
    except Exception as e:
        logging.error(f"An error occurred while running FFmpeg process: {e}")
        raise


async def record_screen(
    output_path,
    audio_codec,
    audio_input,
    video_codec,
    audio_channels,
    input_source,
    loop,
    record_mouse,
    overwrite,
    size,
    framerate,
    duration,
):

    ffmpeg_process = (
        FFmpeg()
        .option("y" if overwrite else "n")
        .input(
            ":0.0+0,0",
            {
                "f": input_source,
                "draw_mouse": int(record_mouse),
                "framerate": framerate,
                "video_size": size,
            },
        )
        .input("default", {"f": audio_input, "ac": audio_channels})
        .output(
            output_path,
            {
                "c:v": video_codec,
                "c:a": audio_codec,
                "t": duration,
            },
        )
    )

    logging.info("FFmpeg command: %s", ffmpeg_process.arguments)

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, run_ffmpeg_process, ffmpeg_process)
