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

import arrc.ops as ops


class MeanInterClassDistance(keras.metrics.Metric):
    def __init__(self, name="mean_inter_class_distance", **kwargs):
        super().__init__(name=name, **kwargs)
        self.total_inter_distance = self.add_weight(name="inter_sum", initializer="zeros")
        self.count = self.add_weight(name="count", initializer="zeros")

    def update_state(self, y_true, y_pred, sample_weight=None):
        labels = keras.ops.cast(y_true, dtype="int32")

        # Compute pairwise cosine distances
        pairwise_distances = 1.0 - keras.ops.matmul(y_pred, keras.ops.transpose(y_pred))

        # Mask for inter-class distances
        inter_mask = keras.ops.not_equal(keras.ops.expand_dims(labels, axis=1), keras.ops.expand_dims(labels, axis=0))

        # Extract inter-class distances
        inter_class_distances = ops.boolean_mask(pairwise_distances, inter_mask)
        inter_mean = keras.ops.mean(inter_class_distances)

        # Update state
        self.total_inter_distance.assign_add(inter_mean)
        self.count.assign_add(1.0)

    def result(self):
        return self.total_inter_distance / self.count

    def reset_states(self):
        self.total_inter_distance.assign(0.0)
        self.count.assign(0.0)
