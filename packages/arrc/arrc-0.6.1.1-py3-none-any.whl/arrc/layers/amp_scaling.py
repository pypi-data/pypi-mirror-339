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
class RandomAmpScalingAugmentation(keras.layers.Layer):
    def __init__(self, min_scale=0.9, max_scale=1.1, likelihood=0.2, **kwargs):
        super().__init__(**kwargs)
        self.min_scale=min_scale
        self.max_scale=max_scale
        self.likelihood=likelihood

    def call(self, inputs, training=None):
        if not training:
            return inputs

        batch_size = keras.ops.shape(inputs)[0]  # dynamic shape

        # Mask batch_size * likelihood rows ...
        mask = keras.random.uniform(shape=[batch_size], dtype="float32")
        mask = keras.ops.less(mask, self.likelihood)
        mask = keras.ops.cast(mask, dtype="int32")

        # Generate the scaling factor for each sample in the batch
        scale_factor_target_shape = (batch_size, *((1,)*(inputs.ndim-1)))
        scale_factor = keras.random.uniform(shape=[batch_size], minval=self.min_scale, maxval=self.max_scale, dtype=inputs.dtype)
        scale_factor = keras.ops.multiply(scale_factor,mask)
        scale_factor = keras.ops.reshape(scale_factor, newshape=scale_factor_target_shape)

        return keras.ops.multiply(inputs, scale_factor)

    def get_config(self):
        config = super().get_config()
        config.update({
            "min_scale": self.min_scale,
            "max_scale": self.max_scale,
            "likelihood": self.likelihood,
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)