import os
import json
import librosa
import numpy as np
import pandas as pd

work_dir="./"

input_dir="../birdclef-2022"

pred = {
    'row_id': [],
    'target': []
}

test_path = input_dir + "/test_soundscapes/"
files = [f.split('.')[0] for f in sorted(os.listdir(test_path))]

birds_path = input_dir + "/scored_birds.json"
with open(birds_path) as bf:
    birds = json.load(bf)

for f in files:
    p = test_path + f + '.ogg'

    d = librosa.get_duration(filename=p)
    pcs = round(d / 5)
    segments = [[] for i in range(pcs)]

    for i in range(len(segments)):
        for b in birds:
            segment_end = (i + 1) * 5
            row_id = f + '_' + b + '_' + str(segment_end)
            pred['row_id'].append(row_id)

            pred['target'].append(True)

cols=['row_id','target']
df_sub=pd.DataFrame(pred,columns=cols)

df_sub.to_csv(work_dir+"/submission.csv", index=False)