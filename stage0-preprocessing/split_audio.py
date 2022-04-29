from pydub import AudioSegment
import math
from os.path import splitext, basename
from pathlib import Path
import logging

logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d ] %(levelname)s %(message)s',
                    datefmt='%d %b %Y,%a %H:%M:%S',
                    filename='split_audio.log',
                    level=logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d ] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


def split_audio(file_path: Path, save_dir: Path):
    """
    input: audio
    output: split 5sec audio
    """

    file_id = splitext(basename(file_path))[0]

    ogg = AudioSegment.from_ogg(file_path)
    dur = math.ceil(len(ogg) / 1000)

    for start_time in range(dur+1):
        # print(start_time)

        if (start_time % 5) != 0:
            continue

        def millisec(time):
            return time * 1000

        end_time = start_time + 5
        l = millisec(start_time)
        r = millisec(end_time)

        # overlap if last window is out of range
        if len(ogg) < 5000:
            while len(ogg) < 5000:
                ogg = ogg + ogg
            piece = ogg[0:5000]
        elif r > len(ogg):
            piece = ogg[-5000:]
        else:
            piece = ogg[l:r]

        save_dir.mkdir(parents=True, exist_ok=True)
        output_filename = file_id + f'_{end_time}.ogg'
        piece.export(save_dir / output_filename, format='ogg')

        logging.info(output_filename + f' | len: {len(piece)}')


if __name__ == '__main__':
    split_audio('./XC216038.ogg')
