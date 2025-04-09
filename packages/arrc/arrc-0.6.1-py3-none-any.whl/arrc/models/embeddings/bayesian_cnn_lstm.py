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

from ..aer_model import ARRCModel
from .embedding_utils import *

def build_bayesian_cnn_lstm_model(
        embedding_dim=128,  # For GSO tuning in external code,
        input_shape=(164 * 30, 1),  # e.g., 30s @164Hz, single channel
        add_noise=True,
        random_shift=True,
        random_amp_scaling=True,
        **arrc_kwargs
):
    """
    Based on the paper:

    Harper, Ross, and Joshua Southern. "A bayesian deep learning framework for end-to-end prediction of emotion
    from heartbeat." IEEE transactions on affective computing 13.2 (2020): 985-991.
    """

    inputs = keras.Input(shape=input_shape)
    augmented = get_augmented_input(inputs, add_noise, random_shift, random_amp_scaling)

    # CNN Stream
    x_cnn = augmented
    x_cnn = keras.layers.Conv1D(128, 8, kernel_initializer="he_normal", activation='relu')(x_cnn)
    x_cnn = keras.layers.Dropout(0.5)(x_cnn, training=True)
    x_cnn = keras.layers.Conv1D(128, 6, kernel_initializer="he_normal", activation='relu')(x_cnn)
    x_cnn = keras.layers.Dropout(0.5)(x_cnn, training=True)
    x_cnn = keras.layers.Conv1D(128, 4, kernel_initializer="he_normal", activation='relu')(x_cnn)
    x_cnn = keras.layers.Dropout(0.5)(x_cnn, training=True)
    x_cnn = keras.layers.Conv1D(128, 2, kernel_initializer="he_normal", activation='relu')(x_cnn)
    x_cnn = keras.layers.Dropout(0.5)(x_cnn, training=True)
    x_cnn = keras.layers.GlobalAveragePooling1D()(x_cnn)

    # LSTM Stream
    x_lstm = keras.layers.MaxPooling1D(pool_size=8)(augmented)
    x_lstm = keras.layers.Bidirectional(keras.layers.LSTM(32, return_sequences=False))(augmented)
    x_lstm = keras.layers.Dropout(0.8)(x_lstm, training=True)

    # Fusion and Output
    x = keras.layers.Concatenate()([x_cnn, x_lstm])
    output = keras.layers.Dense(embedding_dim, activation='relu')(x)

    # Build the model
    return ARRCModel.BuildARRCModel(
        inputs=inputs,
        embedding_outputs=output,
        name="BayesianCNNLSTM",
        num_fc_layers=0,
        **arrc_kwargs,
    )
