import gc

from pydub import AudioSegment
import math
from os.path import splitext, basename
from pathlib import Path


def retrieve_audio(file_path: Path, save_dir: Path, end_time):
    """
    input: audio
    output: split 5sec audio
    """

    file_id = splitext(basename(file_path))[0]

    ogg = AudioSegment.from_ogg(file_path)
    milli_end = end_time * 1000
    piece = ogg[milli_end-5000:milli_end]

    save_dir.mkdir(parents=True, exist_ok=True)
    output_filename = file_id + f'_{end_time}.ogg'
    piece.export(save_dir / output_filename, format='ogg')

