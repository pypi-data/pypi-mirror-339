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


class ArcFace(keras.layers.Layer):
    def __init__(self, num_classes, scale=5.0, **kwargs):
        super(ArcFace, self).__init__(**kwargs)
        self.num_classes = num_classes
        self.scale = scale
        self.W = None
        self._current_batch_y_true = None

    def build(self, input_shape):
        self.W = self.add_weight(
            shape=(input_shape[-1], self.num_classes),
            initializer="glorot_uniform",
            trainable=True
        )

    def call(self, inputs):
        """
        inputs: L2-normalized embeddings (batch_size, embedding_dim) -- must be l2-normalized externally, we're not doing it here.
        Returns: cosine similarity logits (batch_size, num_classes)
        """
        W = ops.l2_normalize(self.W, axis=0)  # Normalize weights
        cosine_logits = keras.ops.matmul(inputs, W) * self.scale  # Scaled cosine similarity

        return cosine_logits
