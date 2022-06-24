import os
import tensorflow as tf
from FCDenseNet import FCDenseNet
from loader import get_dataset

os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate=1e-3,
    decay_steps=1,
    decay_rate=0.995
)
optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
)
checkpointer = tf.keras.callbacks.ModelCheckpoint(
    './checkpoints/',
    save_best_only=True,
    save_weights_only=False,
)
tensorboard = tf.keras.callbacks.TensorBoard(
    './logs',
    write_graph=True,
    write_images=True,
)

model = FCDenseNet([4, 4, 4, 4, 4], 5, 12, 48, 7) # FC-DenseNet57
model.compile(
    optimizer=optimizer,
    loss=tf.keras.losses.SparseCategoricalCrossentropy()
)

train_dataset = get_dataset('*land.tfrecord', './data/v1.0/content/train/')
valid_dataset = get_dataset('*land.tfrecord', './data/v1.0/content/valid/')
test_dataset = get_dataset('*land.tfrecord', './data/v1.0/content/test/')

history = model.fit(train_dataset,
    validation_data=valid_dataset,
    epochs=100, verbose=1,
    callbacks=[early_stopping, checkpointer, tensorboard]
)
model.save_weights('../serving_model/FC-DenseNet57')