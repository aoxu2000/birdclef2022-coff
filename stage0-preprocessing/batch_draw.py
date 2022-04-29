from pathlib import Path
from os import listdir
import logging
from draw import plot_spectrograms
from os.path import splitext, basename
import librosa

# device = 'cuda' if torch.cuda.is_available() else 'cpu'

logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d ] %(levelname)s %(message)s',
                    datefmt='%d %b %Y,%a %H:%M:%S',
                    filename='batch_draw.log',
                    level=logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d ] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


def batch_draw():
    audio_dir = Path('../transdata/train')
    img_dir = Path('../transdata/image')
    # corr_dir = Path('../transdata/corr')

    specs = listdir(audio_dir)
    # species
    for spec in specs:
        name_dir = audio_dir / spec
        for file in listdir(name_dir):
            audio_name = Path(spec) / file

            img_dir.parent.mkdir(parents=True, exist_ok=True)
            # none_path.parent.mkdir(parents=True, exist_ok=True)
            audio_path = audio_dir / audio_name

            d = librosa.get_duration(filename=str(audio_path))
            pcs = round(d / 5)
            for i in range(pcs):
                segment_end = (i + 1) * 5
                img = plot_spectrograms(audio_file=audio_path, endtime=segment_end)
                spec_dir = img_dir / spec
                spec_dir.mkdir(parents=True, exist_ok=True)
                img.save(spec_dir / f'{splitext(basename(audio_name))[0]}_{segment_end}.png')

            logging.info(audio_name)


if __name__ == '__main__':
    batch_draw()
