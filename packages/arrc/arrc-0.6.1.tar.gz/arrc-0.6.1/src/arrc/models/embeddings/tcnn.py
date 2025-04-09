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
from arrc.layers import AttentionPooling1D, GatedConv1D
import keras

from .embedding_utils import *
from ..aer_model import ARRCModel


def _build_tcnn_model(
        input_shape=(5120, 1),  # e.g., 20s @256Hz, single channel
        depth=5,
        num_filters=32,
        dropout_rate=0.1,
        pool_each_block=True,
        add_noise=True,
        random_shift=True,
        random_amp_scaling=True,
):
    """
    Based on the paper:

    T. C. Sweeney-Fanelli and M. H. Imtiaz, "ECG-Based Automated Emotion Recognition Using Temporal Convolution
    Neural Networks," in IEEE Sensors Journal, vol. 24, no. 18, pp. 29039-29046, 15 Sept.15, 2024, doi: 10.1109/JSEN.2024.3434479.
    """

    inputs = keras.layers.Input(shape=input_shape, name="input_signal")

    res = get_augmented_input(inputs, add_noise, random_shift, random_amp_scaling)

    for i in range(depth):
        _, res = GatedConv1D(
            skip_filters=num_filters,
            residual_filters=num_filters*(i+1),
            kernel_size=2,
            strides=1,
            padding='causal',
            dilation_rate=2 ** i,
            last=False, #(i == depth - 1),
        )(res)
        if pool_each_block:
            res = keras.layers.AveragePooling1D(pool_size=2)(res)
            res = keras.layers.Dropout(dropout_rate)(res)

    return inputs, res

def build_tcnn_with_attentionpooling_model(
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
    inputs, output = _build_tcnn_model(input_shape, depth, embedding_dim, dropout_rate, pool_each_block,
                                       add_noise, random_shift, random_amp_scaling)
    output = AttentionPooling1D()(output)
    output = keras.layers.Dense(embedding_dim, activation='relu')(output)
    output = keras.layers.Dropout(dropout_rate)(output)

    return ARRCModel.BuildARRCModel(
        inputs=inputs,
        embedding_outputs=output,
        name="WaveNet",
        num_fc_layers=0,
        **arrc_kwargs,
    )

def build_tcnn_with_globalpooling_model(
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
    inputs, output = _build_tcnn_model(input_shape, depth, embedding_dim, dropout_rate, pool_each_block,
                                       add_noise, random_shift, random_amp_scaling)
    output = keras.layers.GlobalMaxPool1D()(output) if max_pool else keras.layers.GlobalAvgPool1D()(output)
    output = keras.layers.Dense(embedding_dim, activation='relu')(output)
    output = keras.layers.Dropout(dropout_rate)(output)

    return ARRCModel.BuildARRCModel(
        inputs=inputs,
        embedding_outputs=output,
        name="WaveNet",
        num_fc_layers=0,
        **arrc_kwargs,
    )

