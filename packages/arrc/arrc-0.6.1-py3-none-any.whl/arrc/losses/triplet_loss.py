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


class TripletLossWrapper(LossFunctionWrapper):
    def __init__(self, margin, use_semi_hard_negatives, batch_all=False, distance="cosine", reduction="mean"):
        super().__init__(
            fn=TripletLoss(
                margin=margin,
                use_semi_hard_negatives=use_semi_hard_negatives,
                batch_all=batch_all,
                distance=distance),
            reduction=reduction,
            name="triplet_loss",
        )


class TripletLoss(DistanceBasedLoss):
    def __init__(self, margin, use_semi_hard_negatives, batch_all=False, distance="cosine"):
        super(TripletLoss, self).__init__(distance=distance)
        self.margin = margin
        self.use_semi_hard_negatives = use_semi_hard_negatives
        self.batch_all = batch_all

    def __call__(self, labels, embeddings, axis=-1, **kwargs):
        assert (keras.ops.min(keras.ops.cast(labels, "int32")) == 0,
                "Labels must be 0-based indexing")
        loss = self.triplet_loss(labels, embeddings)

        return loss

    def triplet_loss(self, labels, y_pred):
        return self.batch_all_triplet_loss(labels, y_pred) if self.batch_all else self.batch_hard_triplet_loss(labels,
                                                                                                               y_pred)

    def batch_hard_triplet_loss(self, labels, y_pred):
        pairwise_dist = super().pairwise_dist(y_pred)

        # Hardest positive distance
        anchor_positive_dist = self.get_anchor_positive_distances(labels, y_pred, pairwise_dist)

        positive_dist = self.get_hardest_positive_distance(labels, anchor_positive_dist=anchor_positive_dist)
        negative_dist = self.get_hardest_negative_distance(labels, y_pred, pairwise_dist, anchor_positive_dist,
                                                           positive_dist)
        triplet_loss = keras.ops.maximum(positive_dist - negative_dist + self.margin, 0.0)
        triplet_loss = keras.ops.mean(triplet_loss)

        total_loss = triplet_loss
        return total_loss

    def batch_all_triplet_loss(self, labels, y_pred):
        # 1. Compute the pairwise distance matrix (N x N).
        pairwise_distances = super().pairwise_dist(y_pred)
        #   shape: [N, N]

        # 2. Create a mask for valid anchor-positive pairs.
        #    mask[a, p] = True iff labels[a] == labels[p] and a != p
        mask_anchor_positive = self.get_anchor_positive_triplet_mask(labels)
        # shape: [N, N]

        # 3. Create a mask for valid anchor-negative pairs.
        #    mask[a, n] = True iff labels[a] != labels[n]
        mask_anchor_negative = self.get_anchor_negative_triplet_mask(labels)
        # shape: [N, N]

        # 4. For each (a, p) pair, we want to pair with *all* n where the mask says it's a valid negative.
        #   We'll broadcast the distance from a->p against the distance from a->n.

        # Expand dims so we can compare: D(a, p) vs. D(a, n).
        anchor_positive_dist = keras.ops.expand_dims(pairwise_distances, 2)  # shape: [N, N, 1]
        anchor_negative_dist = keras.ops.expand_dims(pairwise_distances, 1)  # shape: [N, 1, N]

        # 5. Compute the triplet loss for *every* possible (a, p, n).
        triplet_loss = anchor_positive_dist - anchor_negative_dist + self.margin
        # shape: [N, N, N]

        # 6. Apply the mask so that only valid (a, p, n) triplets are considered.
        # mask_anchor_positive: shape [N, N]
        # mask_anchor_negative: shape [N, N]
        # We need to combine them into a 3D mask for (a, p, n) because:
        #   - p must be valid positive for a
        #   - n must be valid negative for a
        # So we can do an AND across the expansions:
        mask_ap = keras.ops.expand_dims(mask_anchor_positive, 2)  # shape: [N, N, 1]
        mask_an = keras.ops.expand_dims(mask_anchor_negative, 1)  # shape: [N, 1, N]
        valid_triplets_mask = keras.ops.logical_and(mask_ap, mask_an)
        # shape: [N, N, N]

        if self.use_semi_hard_negatives:
            # For semi-hard negatives:
            #   dist(a, n) > dist(a, p)  AND  dist(a, n) < dist(a, p) + margin
            # We apply this condition as an additional mask:
            semi_hard_mask = keras.ops.logical_and(
                anchor_negative_dist > anchor_positive_dist,
                anchor_negative_dist < anchor_positive_dist + self.margin
            )
            valid_triplets_mask = keras.ops.logical_and(valid_triplets_mask, semi_hard_mask)

        # 7. Zero out invalid triplets
        triplet_loss = keras.ops.where(valid_triplets_mask, triplet_loss, keras.ops.zeros_like(triplet_loss))

        # 8. Apply the hinge, i.e. max(distance, 0)
        triplet_loss = keras.ops.maximum(triplet_loss, 0.0)

        # 9. Count how many triplets actually contributed to the loss
        epsilon = 1e-16  # to avoid dividing by zero if no valid triplets
        valid_triplets = keras.ops.cast(valid_triplets_mask, dtype="float32")
        num_positive_triplets = keras.ops.sum(valid_triplets)

        # 10. Average over all valid triplets
        triplet_loss = keras.ops.sum(triplet_loss) / (num_positive_triplets + epsilon)

        return triplet_loss

    def get_anchor_positive_distances(self, labels, embeddings=None, pairwise_dist=None):
        """
        Returns an NxN matrix where entry [i,j] is the distance between anchor i and embedding j for
        pairs (i,j) such as that i and j belong to the same class. Pairs (i,j) that do not belong
        to the same class are set to 0.0.

        Must provide EITHER embeddings or pairwise_distances. If you already have pairwise_dist it is more
        performant to pass them. Embeddings will only be used to obtain pairwise_distance if needed.

        :param labels:
        :param embeddings:
        :param pairwise_dist:
        :return:
        """
        if pairwise_dist is None:
            if embeddings is None:
                raise ValueError("Either embeddings or pairwise_distance must be provided")

            pairwise_dist = super().pairwise_dist(embeddings)

        mask_anchor_positive = self.get_anchor_positive_triplet_mask(labels)
        mask_anchor_positive = keras.ops.cast(mask_anchor_positive, dtype="float32")
        anchor_positive_dist = keras.ops.multiply(mask_anchor_positive, pairwise_dist)
        return anchor_positive_dist

    def get_hardest_positive_distance(self, labels, pairwise_dist=None, anchor_positive_dist=None):
        """
        Returns a vector where each element, i, i the hardest positive distance for anchor i.
        infinite or 0 distances are both reset to 1e-6 to avoid div-by-zero later.

        Must provide EITHER pairwise distances or anchor_positive_distances... if you already have anchor_positive_dist it is more
        efficient to provide them. We only use pairwise distances to compute anchor positive distances if needed.

        :param labels:
        :param pairwise_dist:
        :param anchor_positive_dist:
        :return:
        """
        if anchor_positive_dist is None:
            if pairwise_dist is None:
                raise ValueError("Either anchor_positive_dist or pairwise_dist must be provided")
            anchor_positive_dist = self.get_anchor_positive_distances(labels, pairwise_dist)

        hardest_positive_dist = keras.ops.max(anchor_positive_dist, axis=1, keepdims=True)
        hardest_positive_dist = keras.ops.where(keras.ops.isinf(hardest_positive_dist),
                                                keras.ops.zeros_like(hardest_positive_dist),
                                                hardest_positive_dist)
        hardest_positive_dist = keras.ops.where(keras.ops.equal(hardest_positive_dist, 0.0),
                                                keras.ops.ones_like(hardest_positive_dist) * 1e-6,
                                                hardest_positive_dist)
        return hardest_positive_dist

    def get_hardest_negative_distance(self, labels, embeddings, pairwise_dist=None, anchor_positive_dist=None,
                                      hardest_positive_dist=None):
        if pairwise_dist is None:
            pairwise_dist = super().pairwise_dist(embeddings)
        if anchor_positive_dist is None:
            anchor_positive_dist = self.get_anchor_positive_distances(labels, pairwise_dist=pairwise_dist)
        if hardest_positive_dist is None:
            hardest_positive_dist = self.get_hardest_positive_distance(labels,
                                                                       anchor_positive_dist=anchor_positive_dist)

        mask_anchor_negative = self.get_anchor_negative_triplet_mask(labels)
        anchor_negative_dist = keras.ops.where(mask_anchor_negative, pairwise_dist, float('inf'))

        if self.use_semi_hard_negatives:
            negatives_mask = keras.ops.logical_and(anchor_negative_dist > hardest_positive_dist,
                                                   anchor_negative_dist < hardest_positive_dist + self.margin)
            anchor_negative_dist = keras.ops.where(negatives_mask, anchor_negative_dist, 1e6)

        result = keras.ops.min(anchor_negative_dist, axis=1, keepdims=True)
        return result

    @staticmethod
    def get_anchor_positive_triplet_mask(labels):
        """Return a 2D mask where mask[a, p] is True iff a and p are distinct and have same label.

        Args:
            labels: int32 `Tensor` with shape [batch_size]

        Returns:
            mask: bool `Tensor` with shape [batch_size, batch_size]
        """
        # Check that i and j are distinct
        indices_equal = keras.ops.cast(keras.ops.eye(keras.ops.shape(labels)[0]), "bool")
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
