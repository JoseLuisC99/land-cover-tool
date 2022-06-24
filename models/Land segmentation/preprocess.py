import os
import pandas as pd
import PIL.Image
import numpy as np


DATA_PATH = os.path.abspath(os.path.join('.', 'data'))
metadata = pd.read_csv(os.path.join(DATA_PATH, 'v0.1', 'metadata.csv'))
train_split = metadata[metadata['split'] == 'train']

OUTPUT_DIR = os.path.join(DATA_PATH, 'v1.0')
IMAGE_SIZE = 320

new_metadata = []
_id = 1
for i in range(len(train_split)):
    _, _, sat_path, mask_path = train_split.iloc[i]
    sat_path = os.path.join(DATA_PATH, 'images', sat_path)
    mask_path = os.path.join(DATA_PATH, 'images', mask_path)
    
    sat_image = PIL.Image.open(sat_path)
    mask_image = PIL.Image.open(mask_path)
    w, h = sat_image.size

    for w_offset in range(0, w, IMAGE_SIZE):
        for h_offset in range(0, h, IMAGE_SIZE):
            if w_offset + IMAGE_SIZE > w or h_offset + IMAGE_SIZE > h:
                continue
            box = (
                w_offset, h_offset, 
                w_offset + IMAGE_SIZE, h_offset + IMAGE_SIZE
            )
            sat_crop = sat_image.crop(box)
            mask_crop = mask_image.crop(box)

            if len(mask_crop.getcolors()) < 3:
                continue

            sat_filename = f'images/{_id}_sat.jpg'
            mask_filename = f'images/{_id}_mask.png'
            sat_crop.save(os.path.join(OUTPUT_DIR, sat_filename))
            mask_crop.save(os.path.join(OUTPUT_DIR, mask_filename))
            new_metadata.append([sat_filename, mask_filename])
            _id = _id + 1
df = pd.DataFrame(new_metadata, columns=['sat_image_path', 'mask_path'])
_split = np.random.choice(['train', 'valid', 'test'], len(new_metadata), p=[0.6, 0.2, 0.2])
df['split'] = _split
df.to_csv(os.path.join(OUTPUT_DIR, 'metadata.csv'), index=False)