import sys

sys.path.append('../input/aoxu-efficientnet/EfficientNet-PyTorch')
sys.path.append('../input/aoxu-efficientnet/EfficientNet-PyTorch/examples/imagenet')

import librosa
import torch
import torchvision.transforms as transforms
from efficientnet_pytorch import EfficientNet
from draw import plot_spectrograms
from pathlib import Path
import json
import os
from torch.utils.data import Dataset, DataLoader
import csv
import cv2
import numpy as np

# ----- offline dir -----

work_dir = "./"
input_dir = Path("../birdclef-2022")
img_dir = Path('./image')
tmp_dir = Path('./splited')
checkpoint_path = './examples/imagenet/model_best.pth.tar'
names_path = './examples/imagenet/names.json'
_batchsize = 4
num_workers = 2

# ----- kaggle dir -----

# work_dir = "/kaggle/working"
# input_dir = Path("/kaggle/input/birdclef-2022")
# img_dir = Path('./image')
# tmp_dir = Path('./splited')
# checkpoint_path = '../input/aoxu-efficientnet/EfficientNet-PyTorch/examples/imagenet/model_best.pth.tar'
# names_path = '../input/aoxu-efficientnet/names.json'
# _batchsize = 32
# num_workers = 4

# ----------------------

test_path = input_dir / "test_soundscapes"


def main():
    with open(names_path, 'r') as n:
        names = json.load(n)

    birds_path = input_dir / "scored_birds.json"
    with open(birds_path, 'r') as bf:
        birds = json.load(bf)

    sub = open('submission.csv', 'w', newline='')
    writer = csv.writer(sub)
    writer.writerow(['row_id', 'target'])

    files = [f.split('.')[0] for f in sorted(os.listdir(test_path))]
    dataset = BirdCLEF(files)
    test_loader = DataLoader(dataset, shuffle=False, batch_size=_batchsize,
                             num_workers=num_workers
                             )

    d = {'num_classes': 21}
    model = EfficientNet.from_name('efficientnet-b3', **d).cuda()
    model = torch.nn.DataParallel(model)
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint['state_dict'])
    model.eval()

    for batch_id, (imgs, fs, segment_ends) in enumerate(test_loader):
        imgs = imgs.cuda()
        _preds = model(imgs)
        ids = _preds.argmax(dim=1).tolist()
        specs = [names[str(_id)] for _id in ids]
        print(specs)
        for i in range(len(specs)):
            spe = specs[i]
            f = fs[i]
            segment_end = segment_ends[i]
            for b in birds:
                row_id = f + '_' + b + '_' + str(int(segment_end.item()))
                if spe == b:
                    pred_target = True
                else:
                    pred_target = False
                writer.writerow([row_id, pred_target])


class BirdCLEF(Dataset):
    def __init__(self, files):
        self.files = files
        self.ids = self.get_ids()

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, item):
        f, segment_end = self.ids[item]
        img = plot_spectrograms(audio_file=test_path / f'{f}.ogg', endtime=segment_end)

        cv2_img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2GRAY)
        mean = cv2.mean(cv2_img)[0]
        img = transforms.ToTensor()(img)
        return img, f, segment_end

    def get_ids(self):
        ids = []
        for f in self.files:
            p = test_path / f'{f}.ogg'
            d = librosa.get_duration(filename=str(p))
            pcs = round(d / 5)
            for i in range(pcs):
                segment_end = (i + 1) * 5
                ids.append((f, segment_end))
        return ids


if __name__ == '__main__':
    main()
