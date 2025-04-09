#  Copyright (c) 2025 - Affects AI LLC
#
#  Licensed under the Creative Common CC BY-NC-SA 4.0 International License (the "License");
#  you may not use this file except in compliance with the License. The full text of the License is
#  provided in the included LICENSE file. If this file is not available, you may obtain a copy of the
#  License at
#
#       https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
#  express or implied. See the License for the specific language governing permissions and limitations
#  under the License.


import arrc
import keras
from keras import layers

from .embedding_utils import *
from ..aer_model import ARRCModel

def build_cnn_model(
        input_shape=None,
        embedding_dim=128,  # For GSO tuning in external code,
        depth=4,
        base_filters=16,
        base_kernel_size=7,
        dropout_rate=0.1,
        add_noise=True,
        random_shift=True,
        random_amp_scaling=True,
        **arrc_kwargs
):
    """
    Builds an ARRCModel with a simple CNN architecture. Each convolution block consists of two convolutional layers,
    followed ReLU activation, dropout, and average pooling.

    This CNN is the baseline model used in the benchmark performance study.

    Each convolutional block doubles the number of filters, and decreases the kernel size by 2, from the previous layer
    each layer. The minimum kernel size is 3.

    Args:
        input_shape: The shape of the input data: (timesteps, channels)
        embedding_dim: The length of the embedding vector
        depth: The number of convolutional blocks in the model
        base_filters: The number of filters in the first convolutional block
        base_kernel_size: The kernel size of the first convolutional block
        dropout_rate: The dropout rate for all dropout layers
        add_noise: if True, add gaussian noise to a random subset of the signals in the input batch using arrc.layers.RandomAdditiveNoise
        random_shift: If True, add a random timeshift to a random subset of the signals in the input batch using arrc.layers.OptimizedRandomShiftAugmentation
        random_amp_scaling: If True, randomly scale the amplitude of a random subset of the signals in the input batch using arrc.layers.RandomAmpScalingAugmentation
        **arrc_kwargs: Additional keyword arguments to pass to ARRCModel.BuildARRCModel
    Returns: an ARRCModel

    """
    inputs = keras.Input(shape=input_shape, name="ecg_input")
    x = get_augmented_input(inputs, add_noise, random_shift, random_amp_scaling)

    # Build N convolutional blocks in a loop
    for i in range(depth):
        # Example: double the filters each time
        filters = base_filters * (2 * (i+1)) 
        # Example: decrease the kernel size by 2 each layer but not below 3
        kernel_size = max(3, base_kernel_size - 2 * i)

        x = layers.Conv1D(filters=filters,
                          kernel_size=kernel_size,
                          strides=1,
                          padding='same')(x)
        x = layers.Conv1D(filters=filters,
                          kernel_size=kernel_size,
                          strides=1,
                          padding='same')(x)
        # x = layers.BatchNormalization()(x)
        # x = layers.LayerNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Dropout(dropout_rate)(x)
        x = layers.AveragePooling1D(pool_size=2)(x)

    # x = layers.GlobalAveragePooling1D()(x)
    x = arrc.layers.AttentionPooling1D()(x)

    # Dense "embedding" layer of size D
    x = layers.Dense(embedding_dim, activation='relu', name="embedding_layer")(x)
    x = layers.Dropout(dropout_rate)(x)

    model = ARRCModel.BuildARRCModel(
        inputs=inputs,
        embedding_outputs=x,
        name="cnn",
        num_fc_layers=0,
        **arrc_kwargs
    )

    return model
