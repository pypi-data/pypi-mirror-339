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

from .distance_loss import DistanceBasedLoss
from .loss_wrapper import LossFunctionWrapper


class ContrastiveLossWrapper(LossFunctionWrapper):
    def __init__(self, margin, distance="cosine", reduction="mean"):
        super().__init__(
            fn=ContrastiveLoss(
                margin=margin,
                distance=distance),
            reduction=reduction,
            name="contrastive_loss",
        )


class ContrastiveLoss(DistanceBasedLoss):
    def __init__(self, margin, distance="cosine"):
        super(ContrastiveLoss, self).__init__(distance=distance)
        self.margin = margin

    def __call__(self, labels, embeddings, axis=-1, **kwargs):
        loss = self.batch_all_contrastive_loss(labels, embeddings)
        return loss

    def batch_all_contrastive_loss(self, labels, y_pred):
        # 1. Compute the pairwise distance matrix (N x N).
        pairwise_distances = super().pairwise_dist(y_pred)
        #   shape: [N, N]

        positive_mask = self.get_anchor_positive_triplet_mask(labels)
        negative_mask = self.get_anchor_negative_triplet_mask(labels)

        # Cast masks into float tensors
        positive_mask = keras.ops.cast(positive_mask, dtype="float32")
        negative_mask = keras.ops.cast(negative_mask, dtype="float32")

        # Positive pairs: Loss = D^2 (squared distance)
        positive_loss = keras.ops.multiply(positive_mask, keras.ops.square(pairwise_distances))
        positive_loss = keras.ops.sum(positive_loss)

        # Negative pairs: Loss = max(margin - D, 0)^2
        negative_loss = keras.ops.multiply(negative_mask,
                                           keras.ops.square(keras.ops.maximum(self.margin - pairwise_distances, 0.0)))
        negative_loss = keras.ops.sum(negative_loss)

        # Normalize by the number of valid pairs (add epsilon to avoid division by zero)
        num_positive_pairs = keras.ops.sum(positive_mask)
        num_negative_pairs = keras.ops.sum(negative_mask)

        epsilon = 1e-16
        loss = (positive_loss / (num_positive_pairs + epsilon)) + (negative_loss / (num_negative_pairs + epsilon))
        return loss

    @staticmethod
    def get_anchor_positive_triplet_mask(labels):
        """Return a 2D mask where mask[a, p] is True iff a and p are distinct and have same label.

        Args:
            labels: int32 `Tensor` with shape [batch_size]

        Returns:
            mask: bool `Tensor` with shape [batch_size, batch_size]
        """
        # Check that i and j are distinct
        indices_equal = keras.ops.cast(keras.ops.eye(keras.ops.shape(labels)[0]), dtype="bool")
        indices_not_equal = keras.ops.logical_not(indices_equal)

        # Check if labels[i] == labels[j]
        # Uses broadcasting where the 1st argument has shape (1, batch_size) and the 2nd (batch_size, 1)
        labels_equal = keras.ops.equal(keras.ops.expand_dims(labels, 0), keras.ops.expand_dims(labels, 1))

        # Combine the two masks
        mask = keras.ops.logical_and(indices_not_equal, labels_equal)

        return mask

    @staticmethod
    def get_anchor_negative_triplet_mask(labels):
        """Return a 2D mask where mask[a, n] is True iff a and n have distinct labels.

        Args:
            labels: int32 `Tensor` with shape [batch_size]

        Returns:
            mask: bool `Tensor` with shape [batch_size, batch_size]
        """
        # Check if labels[i] != labels[k]
        # Uses broadcasting where the 1st argument has shape (1, batch_size) and the 2nd (batch_size, 1)
        labels_equal = keras.ops.equal(keras.ops.expand_dims(labels, 0), keras.ops.expand_dims(labels, 1))
        mask = keras.ops.logical_not(labels_equal)

        return mask
