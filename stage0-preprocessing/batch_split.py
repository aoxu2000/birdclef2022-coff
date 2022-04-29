from os.path import splitext, basename
from os import listdir
from pathlib import Path
from split_audio import split_audio


def batch_split():
    """batch_split"""
    data_dir = Path('../birdclef-2022/train_audio')
    _save_dir = Path('../data')
    names = [name for name in listdir(data_dir) if not name.startswith('.')]
    for name in names:
        name_dir = data_dir / name
        # split_audio(file) for file in listdir(name_dir) if not name.startswith('.')
        for file in listdir(name_dir):
            if not name.startswith('.'):
                file_path = data_dir / name / file
                save_dir = _save_dir / name
                split_audio(file_path, save_dir)


if __name__ == '__main__':
    batch_split()

