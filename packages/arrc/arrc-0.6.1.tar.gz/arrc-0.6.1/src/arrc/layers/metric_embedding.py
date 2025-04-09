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


class MetricEmbedding(keras.layers.Dense):
    """
    This is used as our output layer. If distance metric is cosine, then we l2-normalize the output, otherwise
    this is just a normal dense layer.
    """

    def __init__(self, units, distance_metric, **kwargs):
        super().__init__(units, **kwargs)
        self.distance_metric = distance_metric

    def call(self, inputs, training=False):
        x = super().call(inputs=inputs, training=training)

        if self.distance_metric == "cosine":
            x = keras.ops.norm(x, ord=2, axis=axis, keepdims=keepdims)

        return x
