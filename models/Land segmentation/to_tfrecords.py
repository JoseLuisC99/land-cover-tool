import os
import tensorflow as tf
import pandas as pd

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

def get_split(split, metadata, path):
    # Selecting only train examples
    train_split = metadata[metadata['split'] == split]
    # Output directory
    output_dir = os.path.join(path, 'content', split)
    # Number of images per split for large datasets
    split_size = 100
    n_splits = len(train_split) // split_size
    print(f'Creating {n_splits} splits in {output_dir}')


    for i in range(n_splits):
        _start = i * split_size
        _stop = (i + 1) * split_size
        filename = f'{_start}-{_stop - 1}-land.tfrecord'
        tfrecord_filename = os.path.join(output_dir, filename)
        print(f'Writing ./content/{split}/{filename}')
        # Open tfrecord as writer
        with tf.io.TFRecordWriter(tfrecord_filename) as writer:
            for i in range(_start, _stop):
                image_path, mask_path, _ = train_split.iloc[i]
                # Get satelital and mask image
                image_path = os.path.join(path, image_path)
                mask_path = os.path.join(path, mask_path)
                # Try to read the images
                try:
                    raw_image_file = tf.io.read_file(image_path).numpy()
                    raw_mask_file = tf.io.read_file(mask_path).numpy()
                except FileNotFoundError as e:
                    print(e)
                    continue
                # Create a new example
                example = tf.train.Example(features=tf.train.Features(feature={
                    'sat_image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[raw_image_file])),
                    'mask_image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[raw_mask_file])),
                }))
                # Save the new example in the tfrecord
                writer.write(example.SerializeToString())

if __name__ == '__main__':
    # Data path
    DATA_PATH = os.path.abspath(os.path.join('.', 'data', 'v1.0'))
    # Reading CSV file with dataset info
    metadata = pd.read_csv(os.path.join(DATA_PATH, 'metadata.csv'))
    splits = ['train', 'valid', 'test']
    for split in splits:
        get_split(split, metadata, DATA_PATH)