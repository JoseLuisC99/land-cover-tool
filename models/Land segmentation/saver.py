import os
import tensorflow as tf
from FCDenseNet import FCDenseNet

os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

if __name__ == '__main__':
    print('Loading weights...')
    model = FCDenseNet([4, 4, 4, 4, 4], 5, 12, 48, 7)
    model.load_weights('./weights/FC-DenseNet57')
    model.compute_output_shape(input_shape=(None, None, None, 3))

    MODEL_DIR = os.path.join('..', 'serving_models', 'land-cover')
    VERSION = 1
    export_path = os.path.join(MODEL_DIR, str(VERSION))
    print(f'Export path = {export_path}')

    tf.keras.models.save_model(
        model,
        export_path,
        overwrite=True,
        include_optimizer=True,
        save_format=None,
        signatures=None,
        options=None
    )
    print('Model saved:')
    print(os.system(f'ls -l {export_path}'))