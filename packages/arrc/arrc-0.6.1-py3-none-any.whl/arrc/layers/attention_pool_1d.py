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

@keras.saving.register_keras_serializable(package="ARRCLayers")
class AttentionPooling1D(keras.layers.Layer):
    def __init__(self, output_dim=32):
        super(AttentionPooling1D, self).__init__()
        self.output_dim = output_dim
        self.attention_score = keras.layers.Dense(1, activation=None)  # Learnable attention weights
        self.attention_weight = keras.layers.Softmax(axis=1)
        self.multiply = keras.layers.Multiply()
        self.pool = keras.layers.Lambda(lambda z: keras.ops.sum(z, axis=1), name="att_pool",
                                        output_shape=(output_dim,))

    def call(self, inputs):
        attention_scores = self.attention_score(inputs)  # Compute attention scores
        attention_weights = self.attention_weight(attention_scores)  # Normalize across time
        weighted_output = self.multiply([inputs, attention_weights])  # Apply weights
        return self.pool(weighted_output)

    def get_config(self):
        config = super().get_config()
        config.update({
            "output_dim": self.output_dim
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)