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


import keras

from arrc.models.aer_model import ARRCModel
from arrc.models.embeddings.embedding_utils import get_augmented_input


def res_block(x, num_filters=32, ):
    block = x
    block = keras.layers.Conv1D(filters=num_filters, kernel_size=3, strides=1, padding='same')(block)
    block = keras.layers.BatchNormalization()(block)
    block = keras.layers.ReLU()(block)
    block = keras.layers.Conv1D(filters=num_filters, kernel_size=3, strides=1, padding='same')(block)
    block = keras.layers.Add()([x, block])
    block = keras.layers.BatchNormalization()(block)

    result = keras.layers.ReLU()(block)
    result = keras.layers.BatchNormalization()(result)
    result = keras.layers.MaxPooling1D(pool_size=2)(result)

    return result


def build_resnet_cnn_model(
        input_shape=(5120, 1),  # e.g., 20s @256Hz, single channel
        num_classes=None,
        num_filters=32,
        dropout_rate=0.1,
        add_noise=True,
        random_shift=True,
        random_amp_scaling=True,
        **kwargs,
):
    inputs = keras.layers.Input(shape=input_shape, name="input_signal")
    aug = get_augmented_input(inputs, add_noise, random_shift, random_amp_scaling)

    blocks = res_block(aug, num_filters=num_filters)
    blocks = keras.layers.Dropout(dropout_rate)(blocks)
    # blocks = res_block(blocks, num_filters=num_filters)
    # blocks = keras.layers.Dropout(dropout_rate)(blocks)
    blocks = res_block(blocks, num_filters=num_filters)
    blocks = keras.layers.Dropout(dropout_rate)(blocks)
    blocks = res_block(blocks, num_filters=num_filters)
    blocks = keras.layers.Dropout(dropout_rate)(blocks)
    # output = layers.AttentionPooling1D()(blocks)
    output = keras.layers.GlobalAveragePooling1D()(blocks)
    output = keras.layers.Dense(units=num_filters, activation="relu")(output)

    model = ARRCModel.BuildARRCModel(
        inputs=inputs,
        embedding_outputs=output,
        num_classes=num_classes,
        name="resnet",
        num_fc_layers=0,
        **kwargs
    )

    return model
