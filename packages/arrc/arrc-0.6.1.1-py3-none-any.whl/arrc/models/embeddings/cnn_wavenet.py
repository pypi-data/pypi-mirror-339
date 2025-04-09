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
import arrc.layers
import keras

from .embedding_utils import *
from ..aer_model import ARRCModel


def _build_cnn_wavenet_model(
        input_shape=(5120, 1),  # e.g., 20s @256Hz, single channel
        depth=5,
        num_filters=32,
        dropout_rate=0.1,
        pool_each_block=True,
        add_noise=True,
        random_shift=True,
        random_amp_scaling=True,
):
    inputs = keras.layers.Input(shape=input_shape, name="input_signal")

    skips=[]
    res = get_augmented_input(inputs, add_noise, random_shift, random_amp_scaling)

    for i in range(depth):
        skip, res = arrc.layers.GatedConv1D(residual_filters=num_filters, skip_filters=num_filters, kernel_size=2, strides=1, padding='causal', dilation_rate=2 ** i, last=i==(depth-1))(res)
        skips.append(skip)

    skip_sum = keras.layers.Add(name="skip_sum")(skips)
    return inputs, skip_sum

def build_cnn_wavenet_with_attentionpooling_model(
        input_shape=(5120, 1),  # e.g., 20s @256Hz, single channel
        depth=5,
        embedding_dim=32,
        dropout_rate=0.1,
        pool_each_block=True,
        add_noise=True,
        random_shift=True,
        random_amp_scaling=True,
        **arrc_kwargs
):
    inputs, output = _build_cnn_wavenet_model(input_shape, depth, embedding_dim, dropout_rate, pool_each_block, add_noise, random_shift, random_amp_scaling)
    output = arrc.layers.AttentionPooling1D()(output)
    output = keras.layers.Dense(embedding_dim, activation='relu')(output)
    output = keras.layers.Dropout(dropout_rate)(output)
    return ARRCModel.BuildARRCModel(
        inputs=inputs,
        embedding_outputs=output,
        name="WaveNet",
        num_fc_layers=0,
        **arrc_kwargs,
    )

def build_cnn_wavenet_with_globalpooling_model(
        input_shape=(5120, 1),  # e.g., 20s @256Hz, single channel
        depth=5,
        embedding_dim=32,
        dropout_rate=0.1,
        pool_each_block=True,
        max_pool=True,
        add_noise=True,
        random_shift=True,
        random_amp_scaling=True,
        **arrc_kwargs
):
    inputs, output = _build_cnn_wavenet_model(input_shape, depth, embedding_dim, dropout_rate, pool_each_block, add_noise, random_shift,
                                              random_amp_scaling)
    output = keras.layers.GlobalMaxPool1D()(output) if max_pool else keras.layers.GlobalAvgPool1D()(output)
    output = keras.layers.Dense(embedding_dim)(output)
    output = keras.layers.LayerNormalization()(output)
    output = keras.layers.ReLU()(output)
    output = keras.layers.Dropout(dropout_rate)(output)
    return ARRCModel.BuildARRCModel(
        inputs=inputs,
        embedding_outputs=output,
        name="WaveNet",
        num_fc_layers=0,
        **arrc_kwargs,
    )

