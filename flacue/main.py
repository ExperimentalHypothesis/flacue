#!/usr/bin/env python3

import argparse
import logging
import os.path
from subprocess import CompletedProcess, CalledProcessError, run

from ffcuesplitter.exceptions import FFMpegError

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)



def split_on_cue(cue_file_path: str) -> CompletedProcess[bytes]:
    """
    Splits files based on a cue file.
    """
    cmd = ["ffcuesplitter", "-i", cue_file_path]
    try:
        result = run(cmd, check=True)
    except CalledProcessError as err:
        raise FFMpegError(f"Splitting cue {cue_file_path} failed with {err}") from err
    except FileNotFoundError as err:
        raise FFMpegError(f"Splitting cue {cue_file_path} failed with {err}") from err
    except KeyboardInterrupt as err:
        msg = "[KeyboardInterrupt] process failed."
        raise FFMpegError(msg) from err
    return result


def remove_original_audio_file(cue_file_path: str) -> None:
    """
    Delete original audiofile.
    There is a precondition that the name of the file matches the name of the CUE file.
    """
    original_audio_file = get_original_audio_file(cue_file_path)
    try:
        # os.remove(original_audio_file)
        logger.info(f"Deleted original audiofile {original_audio_file}")
    except OSError as e:
        logger.error(f"Error deleting original audiofile {original_audio_file}: {e}")


def get_original_audio_file(cue_file_path: str) -> str:
    """
    Get the original audio file.
    """
    extensions = [".flac", ".alac", ".ape"]

    file_without_ext = os.path.splitext(cue_file_path)[0]
    file_with_ext = ""
    for ext in extensions:
        file_with_ext = file_without_ext + ext
        if not os.path.exists(file_with_ext):
            continue
        else:
            break
    return file_with_ext



def parse_args():
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description="Process a file.")
    parser.add_argument("filepath", help="Path to the file to be processed")
    parser.add_argument("-ro", "--remove-original", action="store_true",
                        help="Remove the original file after processing", default=False)

    return parser.parse_args()


def main():
    """
    Entrypoint.
    """
    args = parse_args()
    cue_file_path = args.filepath
    remove_original = args.remove_original

    result = split_on_cue(cue_file_path)
    if result.returncode == 0 and remove_original == True:
        remove_original_audio_file(cue_file_path)

    logger.info("----- ALL DONE SUCCESSFULLY -----")


if __name__ == "__main__":
    main()