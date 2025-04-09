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
class GatedConv1D(keras.layers.Layer):
    def __init__(self, residual_filters, kernel_size, skip_filters = None, last=False, noskip=False, **conv_kwargs):
        super().__init__()
        if skip_filters is None:
            skip_filters = residual_filters

        self.last = last
        self.conv = keras.layers.Conv1D(filters=residual_filters*2, kernel_initializer='he_uniform', kernel_size=kernel_size, **conv_kwargs)
        self.skip_conv = keras.layers.Conv1D(filters=skip_filters, kernel_initializer='he_uniform', kernel_size=1, padding="same")
        self.res_conv = keras.layers.Conv1D(filters=residual_filters, kernel_initializer='he_uniform', kernel_size=1, padding="same")
        self.add = keras.layers.Add()

        self.conv_kwargs = {}
        self.conv_kwargs.update(conv_kwargs)

    def call(self, inputs, training=None):
        return self._call(inputs, training) if not self.last else self._last_call(inputs, training)

    def _last_call(self, inputs, training=None):
        x = self.conv(inputs)
        filters, gates = keras.ops.split(x, 2, axis=-1)
        z = keras.ops.multiply(keras.ops.tanh(filters), keras.ops.sigmoid(gates))
        skip = self.skip_conv(z)
        return skip, None

    def _call(self, inputs, training=None):
        x = self.conv(inputs)
        filters, gates = keras.ops.split(x, 2, axis=-1)
        z = keras.ops.multiply(keras.ops.tanh(filters), keras.ops.sigmoid(gates))

        skip = self.skip_conv(z)
        res = self.add([z,self.res_conv(inputs)])

        return skip, res

    def build(self, input_shape):
        self.conv.build(input_shape)
        conv_out_shape = self.conv.compute_output_shape(input_shape)
        conv_out_shape = (conv_out_shape[0], conv_out_shape[1], conv_out_shape[2]//2)

        if not self.last:
            self.res_conv.build(input_shape)

        self.skip_conv.build(conv_out_shape)

        self.add.build((conv_out_shape, conv_out_shape))
        super().build(input_shape)
        self.built = True


    def compute_output_shape(self, input_shape):
        skip_shape = self.skip_conv.compute_output_shape(input_shape)
        res_shape = self.res_conv.compute_output_shape(input_shape)
        return (skip_shape, res_shape )


    def get_config(self):
        config = super().get_config()
        config.update({
            "kernel_size": self.conv.kernel_size[0],  # for 1D
            "residual_filters": self.conv.filters // 2,  # or store separately
            "skip_filters": self.skip_conv.filters,
            "last": self.last,
        })
        config.update(self.conv_kwargs)
        return config

    @classmethod
    def from_config(cls, config):
        # Create the instance
        layer = cls(
            **config,  # if any extra kwargs in config
        )


        return layer