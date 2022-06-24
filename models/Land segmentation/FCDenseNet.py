import tensorflow as tf
from tensorflow.keras.layers import BatchNormalization, Activation, Conv2D, Dropout, MaxPool2D, Conv2DTranspose, InputLayer, Softmax

class ConvBlock(tf.keras.Model):
    def __init__(self, growth_rate, dropout_rate, name=''):
        super(ConvBlock, self).__init__(name=name)
        self.bn = BatchNormalization()
        self.activ = Activation('relu')
        self.conv = Conv2D(growth_rate, 3, padding='same', kernel_initializer='he_normal')
        self.dropout = Dropout(dropout_rate)
    def call(self, input_tensor, training=False):
        x = self.bn(input_tensor, training=training)
        x = self.activ(x)
        x = self.conv(x)
        return self.dropout(x)

class DenseBlock(tf.keras.Model):
    def __init__(self, layers, growth_rate, dropout_rate, name=''):
        super(DenseBlock, self).__init__(name=name)
        self.conv_layers = []
        for _ in range(layers):
            self.conv_layers.append(ConvBlock(growth_rate, dropout_rate))
    def call(self, input_tensor, training=False):
        dense_out = []
        x = input_tensor
        for layer in self.conv_layers:
            layer_out = layer(x)
            x = tf.concat([x, layer_out], axis=3)
            dense_out.append(layer_out)
        return tf.concat(dense_out, axis=3)

class TransitionDown(tf.keras.Model):
    def __init__(self, filters, dropout_rate, name=''):
        super(TransitionDown, self).__init__(name=name)
        self.bn = BatchNormalization()
        self.activ = Activation('relu')
        self.conv = Conv2D(filters, 1, padding='same', kernel_initializer='he_normal')
        self.dropout = Dropout(dropout_rate)
        self.maxpool = MaxPool2D()
    def call(self, input_tensor, training=False):
        x = self.bn(input_tensor, training=training)
        x = self.activ(x)
        x = self.conv(x)
        x = self.dropout(x)
        return self.maxpool(x)

class TransitionUp(tf.keras.Model):
    def __init__(self, filters, name=''):
        super(TransitionUp, self).__init__(name=name)
        self.trans_conv = Conv2DTranspose(filters, 3, 2, padding='same', kernel_initializer='he_normal')
    def call(self, input_tensor, training=False):
        x = self.trans_conv(input_tensor)
        return x

class FCDenseNet(tf.keras.Model):
    def __init__(self, 
        layers_per_denseblock, layers_in_bottleneck,
        growth_rate, n_filters_first_conv, n_classes,
        in_channels=3, dropout_rate = 0.2, name=''
    ):
        super(FCDenseNet, self).__init__(name=name)

        # Input layer
        self.input_layer = InputLayer(input_shape=(None, None, None, in_channels))
        
        # First convolution
        self.first_conv = Conv2D(n_filters_first_conv, 3, padding='same', kernel_initializer='he_normal', name='first_convolution')
        
        # Encoder layers
        _n_filters = n_filters_first_conv
        self.encoder_dense_layers = []
        for idx, layers in enumerate(layers_per_denseblock):
            db_layer = DenseBlock(layers, growth_rate, dropout_rate, name=f'encoder_DB_{idx}')
            _n_filters += layers * growth_rate
            td_layer = TransitionDown(_n_filters, dropout_rate, name=f'encoder_TD_{idx}')
            self.encoder_dense_layers.append((db_layer, td_layer))
        
        # Bottleneck layer
        self.bottleneck = DenseBlock(layers_in_bottleneck, growth_rate, dropout_rate, name='bottleneck')

        # Decoder layers
        layers_per_denseblock.reverse()
        _n_filters = layers_in_bottleneck * growth_rate
        self.decoder_dense_layers = []
        for idx, layers in enumerate(layers_per_denseblock):
            tu_layer = TransitionUp(_n_filters, name=f'decoder_TU_{idx}')
            db_layer = DenseBlock(layers, growth_rate, dropout_rate, name=f'dencoder_DB_{idx}')
            _n_filters = layers * growth_rate
            self.decoder_dense_layers.append((tu_layer, db_layer))
        
        # Classifier + Softmax layer
        self.last_conv = Conv2D(n_classes, 1, padding='same', kernel_initializer='glorot_uniform', name='first_convolution')
        self.segmentation_layer = Softmax()
        
    def call(self, input_tensor, training=False):
        x = self.input_layer(input_tensor)
        x = self.first_conv(x)
        
        skip_connections = []
        for db_layer, td_layer in self.encoder_dense_layers:
            dense = db_layer(x)
            x = tf.concat([x, dense], axis=3)
            skip_connections.append(x)
            x = td_layer(x)
        skip_connections.reverse()
        
        x = self.bottleneck(x)

        for idx, (tu_layer, db_layer) in enumerate(self.decoder_dense_layers):
            x = tu_layer(x)
            x = tf.concat([x, skip_connections[idx]], axis=3)
            x = db_layer(x)
        
        x = self.last_conv(x)
        x = self.segmentation_layer(x)
        return x