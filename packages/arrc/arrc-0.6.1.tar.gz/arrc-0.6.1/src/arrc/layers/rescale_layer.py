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
class RescaleToRange(keras.layers.Layer):
    """
    Rescale each individual input in the batch to the range [new_min, new_max].
    By default, reduces over all dimensions except the first (batch dimension).

    Arguments:
    - new_min (float): The lower bound of the new range.
    - new_max (float): The upper bound of the new range.
    - axis (list or int): The axes over which to compute min/max.
      If None, defaults to all axes except the first (batch axis).
    - epsilon (float): Small number to avoid divide-by-zero.
    """

    def __init__(self, new_min=-1.0, new_max=1.0, axis=1, epsilon=1e-7, **kwargs):
        super(RescaleToRange, self).__init__(**kwargs)
        self.new_min = new_min
        self.new_max = new_max
        self.axis = axis
        self.epsilon = epsilon

    def call(self, inputs):
        x_min = keras.ops.min(inputs, axis=self.axis, keepdims=True)
        x_max = keras.ops.max(inputs, axis=self.axis, keepdims=True)

        x_norm = (inputs - x_min) / (x_max - x_min + self.epsilon)
        x_scaled = x_norm * (self.new_max - self.new_min) + self.new_min
        return x_scaled

    def get_config(self):
        # Necessary to support serialization of the layer
        config = super(RescaleToRange, self).get_config()
        config.update({
            "new_min": self.new_min,
            "new_max": self.new_max,
            "axis": self.axis,
            "epsilon": self.epsilon
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)