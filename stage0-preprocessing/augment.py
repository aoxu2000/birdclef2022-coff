import cv2
from pathlib import Path
from os import listdir
from shutil import move
import logging
from os import remove
import cv2
import numpy as np
from numpy import random
import math
from torchvision import transforms
from os.path import basename, splitext


logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d ] %(levelname)s %(message)s',
                    datefmt='%d %b %Y,%a %H:%M:%S',
                    filename='augment.log',
                    level=logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d ] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


# 随机亮度增强（random brightness）
class RandomBrightness(object):
    def __init__(self, delta=10):
        assert delta >= 0
        assert delta <= 255
        self.delta = delta

    def __call__(self, image):
        if random.randint(2):
            delta = random.uniform(-self.delta, self.delta)
            image = (image + delta).clip(0.0, 255.0)
            # print('RandomBrightness,delta ',delta)
        return image


# 随机对比度增强（random contrast）
class RandomContrast(object):
    def __init__(self, lower=0.9, upper=1.05):
        self.lower = lower
        self.upper = upper
        assert self.upper >= self.lower, "contrast upper must be >= lower."
        assert self.lower >= 0, "contrast lower must be non-negative."

    # expects float image
    def __call__(self, image):
        if random.randint(2):
            alpha = random.uniform(self.lower, self.upper)
            # print('contrast:', alpha)
            image = (image * alpha).clip(0.0, 255.0)
        return image


# 随机饱和度增强（random saturation）
class RandomSaturation(object):
    def __init__(self, lower=0.8, upper=1.2):
        self.lower = lower
        self.upper = upper
        assert self.upper >= self.lower, "contrast upper must be >= lower."
        assert self.lower >= 0, "contrast lower must be non-negative."

    def __call__(self, image):
        if random.randint(2):
            alpha = random.uniform(self.lower, self.upper)
            image[:, :, 1] = image[:, :, 1] * alpha
            # print('RandomSaturation,alpha',alpha)
        return image


def main():
    data_dir = Path('../data/corr')
    specs = listdir(data_dir)

    rb = RandomBrightness()
    rc = RandomContrast()
    rs = RandomSaturation()

    for spec in specs:
        files = listdir(data_dir / spec)
        cnt = 0
        while len(files) < 1000:
            cnt = cnt + 1
            # file_cnt = len(files)
            for file in files:

                # file_cnt += 1
                # if file_cnt > 1000:
                #     break

                if '(' in file:
                    continue
                file_path = data_dir / spec / file
                img = cv2.imread(str(file_path))

                img = rb(img)
                img = rc(img)
                img = rs(img)

                basename_ = basename(file)
                write_file = splitext(basename_)[0] + f'({str(cnt)})' + splitext(basename_)[1]
                dest = data_dir / spec / write_file
                cv2.imwrite(str(dest), img)
                logging.info(dest)
            files = listdir(data_dir / spec)


if __name__ == '__main__':
    main()
