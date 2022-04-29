from pathlib import Path
from os import listdir
import logging


logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d ] %(levelname)s %(message)s',
                    datefmt='%d %b %Y,%a %H:%M:%S',
                    filename='statis.log',
                    level=logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d ] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


def main():
    data_dir = Path('../data/corr')
    # none_dir = Path('../data/corr/none')
    specs = listdir(data_dir)
    for spec in specs:
        files = listdir(data_dir / spec)
        logging.info(f'{spec}: {len(files)}')


if __name__ == '__main__':
    main()
