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
class RandomAdditiveNoise(keras.layers.Layer):
    def __init__(self, noise_max_std_dev=0.02, likelihood=0.2, **kwargs):
        super().__init__(**kwargs)
        self.noise_max_std_dev=noise_max_std_dev
        self.likelihood=likelihood

    def call(self, inputs, training=None):
        if not training:
            return inputs

        input_shape = keras.ops.shape(inputs)
        batch_size = input_shape[0]  # dynamic shape

        mask = keras.random.uniform(shape=[batch_size], dtype="float32")
        mask = keras.ops.less(mask, self.likelihood)
        mask = keras.ops.cast(mask, dtype="int32")
        mask = keras.ops.reshape(mask, newshape=(batch_size, *((1,)*(inputs.ndim-1))))

        # Mask batch_size * likelihood rows ...
        noise_std = keras.random.uniform(shape=(1,), minval=0.0, maxval=self.noise_max_std_dev)[0]
        noise = keras.random.normal(shape=input_shape, stddev=noise_std, dtype="float32")
        noise = keras.ops.multiply(noise, mask)

        return keras.ops.add(inputs, noise)

    def get_config(self):
        config = super().get_config()
        config.update({
            "noise_max_std_dev": self.noise_max_std_dev,
            "likelihood": self.likelihood,
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)