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
from keras import layers
from pytorch_metric_learning.utils.distributed import gather_enqueue_mask


@keras.saving.register_keras_serializable(package="ARRCLayers")
class OptimizedRandomShiftAugmentation(layers.Layer):
    """
    Shifts a fraction of the batch's time-series signals to the right by a random number of steps.
    The newly exposed left portion is padded with the row's mean.
    """
    def __init__(self, max_shift=0.1, likelihood=0.2, **kwargs):
        super().__init__(**kwargs)
        self.max_shift_fraction = max_shift   # fraction of time_steps to shift
        self.likelihood = likelihood

    def call(self, x, training=None):
        # Only do augmentation during training
        if training is False:
            return x


        # x: shape = [batch_size, time_steps] (assuming 2D)
        batch_size = keras.ops.shape(x)[0]
        time_steps = keras.ops.shape(x)[1]
        channels = keras.ops.shape(x)[2]

        # 1) Decide which rows to shift
        #    mask[b] = True with probability self.likelihood
        mask = keras.random.uniform(shape=[batch_size]) < self.likelihood

        # 2) Compute a random shift amount for each row (in [0, max_shift])
        #    We'll convert max_shift_fraction to an integer # steps
        #    e.g. if T=1000 and max_shift_fraction=0.1 => max_shift_steps=100
        max_shift_steps = keras.ops.cast(self.max_shift_fraction * keras.ops.cast(time_steps, "float32"), "int32")

        shift_amounts = keras.random.randint(
            minval=0,
            maxval=max_shift_steps + 1,
            shape=[batch_size],
            dtype="int32",
        )

        # For rows that are NOT shifting, we set shift_amount=0
        shift_amounts = keras.ops.where(mask, shift_amounts, keras.ops.zeros_like(shift_amounts))

        # 5) For indices that were < 0, we fill with that row's mean
        #    row_means: shape [B], broadcast to [B, T]
        row_means = keras.ops.mean(x, axis=1,keepdims=True)  # shape [B]
        row_means = keras.ops.broadcast_to(row_means, [batch_size, time_steps, channels])  # shape [B,T,channels]

        # 3) Build an index for each (batch, time) to know which original column to gather.
        #    new_col[b, t] = t - shift_amounts[b]
        time_indices = keras.ops.arange(time_steps)  # shape [T]
        time_indices = keras.ops.reshape(time_indices, [1, time_steps,1])  # shape [1, T,1]
        shift_amounts_2d = keras.ops.reshape(shift_amounts, [batch_size, 1,1])  # shape [B, 1,1]
        new_col = time_indices - shift_amounts_2d  # shape [B, T,1]

        # We'll gather from x only where new_col >= 0; otherwise, it means we've "fallen off" the left side.
        is_valid = (new_col >= 0)  # shape [B, T, 1]
        # We'll clamp negative indices to 0 temporarily for the gather step
        clamped_col = keras.ops.where(is_valid, new_col, keras.ops.zeros_like(new_col))

        # 4) Flatten x and gather
        #    x_flat: shape [B*T], index(b, t) = b*T + clamped_col[b, t]
        x_flat = keras.ops.reshape(keras.ops.transpose(x,axes=[0,2,1]), [batch_size*time_steps*channels])  # flatten

        # row_indices[b] = b
        row_indices = keras.ops.arange(batch_size*channels)
        row_indices_2d = keras.ops.reshape(row_indices, [batch_size, 1,channels])  # shape [B, 1]
        row_indices_broadcast = row_indices_2d * time_steps  # shape [B, 1]
        gather_indices = row_indices_broadcast + clamped_col  # shape [B, T]
        gather_indices_flat = keras.ops.reshape(gather_indices, [batch_size * time_steps * channels])  # shape [B*T]


        gathered_flat = keras.ops.take(x_flat, gather_indices_flat,axis=0)  # shape [B*T]
        gathered_2d = keras.ops.reshape(gathered_flat, [batch_size, time_steps, channels])


        shifted = keras.ops.where(is_valid, gathered_2d, row_means)

        return shifted

    def get_config(self):
        config = super().get_config()
        config.update({
            "max_shift": self.max_shift_fraction,
            "likelihood": self.likelihood,
        })
        return config


    @classmethod
    def from_config(cls, config):
        return cls(**config)