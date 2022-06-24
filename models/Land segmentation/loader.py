import tensorflow as tf
import glob

CLASS_COLOR = [
    tf.constant([0, 255, 255], dtype=tf.uint8),     # urban_land
    tf.constant([255, 255, 0], dtype=tf.uint8),     # agriculture_land
    tf.constant([255, 0, 255], dtype=tf.uint8),     # rangeland
    tf.constant([0, 255, 0], dtype=tf.uint8),       # forest_land
    tf.constant([0, 0, 255], dtype=tf.uint8),       # water
    tf.constant([255, 255, 255], dtype=tf.uint8),   # barren_land
    tf.constant([0, 0, 0], dtype=tf.uint8),         # unknown
]

def decode_tfrecord(record):
    return tf.io.parse_single_example(
        record,
        {
            'sat_image': tf.io.FixedLenFeature([], dtype=tf.string),
            'mask_image': tf.io.FixedLenFeature([], dtype=tf.string),
        }
    )

def preprocess_data(sample):
    sat_image = tf.image.decode_image(sample['sat_image'], channels=3)
    mask_image = tf.image.decode_image(sample['mask_image'], channels=3)
    tf.Tensor.set_shape(sat_image, (320, 320, 3))
    tf.Tensor.set_shape(mask_image, (320, 320, 3))

    mask_layer = tf.zeros((320, 320), dtype=tf.uint8)
    for idx, class_color in enumerate(CLASS_COLOR):
        _mask = mask_image == class_color
        _mask = tf.reduce_all(_mask, axis=2)
        _mask = tf.where(_mask, idx, 0)
        _mask = tf.cast(_mask, tf.uint8)
        mask_layer = mask_layer + _mask
    
    sat_image = tf.cast(sat_image, tf.float32)
    return sat_image, mask_layer
    
def get_dataset(pattern, tfr_dir):
    files = glob.glob(tfr_dir + pattern, recursive=False)
    dataset = tf.data.TFRecordDataset(files)

    autotune = tf.data.AUTOTUNE
    dataset = dataset.map(decode_tfrecord, num_parallel_calls=autotune)
    dataset = dataset.map(preprocess_data, num_parallel_calls=autotune)
    dataset = dataset.shuffle(16)
    dataset = dataset.batch(3, drop_remainder=True)
    dataset = dataset.prefetch(autotune)

    return dataset