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

import arrc.ops as ops
import keras


@keras.saving.register_keras_serializable(package="ARRCLayers")
class NanCheckLayer(keras.layers.Layer):
    def __init__(self, input_shape, **kwargs):
        super().__init__(**kwargs)
        self.input_shape = input_shape

    def call(self, inputs, training=None):
        if keras.ops.any(keras.ops.isinf(inputs)):
            print(inputs)
            raise ValueError(f"Inf detected in layer {self.name}")
        if keras.ops.any(keras.ops.isnan(inputs)):
            print(inputs)
            raise ValueError(f"NaN detected in layer {self.name}")
        return inputs

    def compute_output_shape(self, *args, **kwargs):
        return self.input_shape

    def get_config(self):
        config = super().get_config()
        config.update({"input_shape": self.input_shape})
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)