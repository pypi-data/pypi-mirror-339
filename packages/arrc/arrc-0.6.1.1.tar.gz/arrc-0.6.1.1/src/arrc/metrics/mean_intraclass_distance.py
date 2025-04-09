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


class MeanIntraClassDistance(keras.metrics.Metric):
    def __init__(self, name="intra_inter_distance", num_classes=2, **kwargs):
        super().__init__(name=name, **kwargs)
        self.num_classes = num_classes
        self.intra_distances = self.add_weight(name="intra", initializer="zeros")
        self.count = self.add_weight(name="count", initializer="zeros")

    def update_state(self, y_true, y_pred, sample_weight=None):
        labels = keras.ops.cast(y_true, dtype="int32")  # Ensure integer labels

        # Compute pairwise cosine distances (1 - cosine similarity)
        pairwise_distances = 1.0 - keras.ops.matmul(y_pred, keras.ops.transpose(y_pred))

        # Create masks for intra-class
        label_matrix = keras.ops.equal(keras.ops.expand_dims(labels, axis=1), keras.ops.expand_dims(labels, axis=0))
        intra_mask = keras.ops.logical_and(label_matrix,
                                           keras.ops.logical_not(
                                               keras.ops.eye(keras.ops.shape(labels)[0],
                                                             dtype="bool")))  # Remove self-distances

        # Apply masks to extract intra-class and inter-class distances
        intra_class_distances = ops.boolean_mask(pairwise_distances, intra_mask)

        # Compute mean distances
        intra_mean = keras.ops.mean(intra_class_distances)

        # Update state variables
        self.intra_distances.assign_add(intra_mean)
        self.count.assign_add(1.0)

    def result(self):
        return self.intra_distances / self.count

    def reset_states(self):
        self.intra_distances.assign(0.0)
        self.count.assign(0.0)
