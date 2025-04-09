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


from abc import abstractmethod

import arrc.ops as ops
import keras
import numpy as np
import tensorflow as tf
import torch.distributed as dist

from .distance_loss import DistanceBasedLoss
from .loss_wrapper import LossFunctionWrapper


class CenterTripletLossWrapper(LossFunctionWrapper, keras.callbacks.Callback):
    def __init__(self, num_classes, embedding_dim, square_distances=False, margin=0.1, alpha=0.01,
                 center_movement=False, reduction="sum_over_batch_size"):
        super().__init__(
            fn=CenterTripletLoss(
                num_classes=num_classes,
                embedding_dim=embedding_dim,
                margin=margin,
                alpha=alpha,
                center_movement=center_movement),
            reduction=reduction,
            name="center_triplet_loss",
            axis=-1
        )

    @property
    def current_centers(self):
        return self.fn.current_centers

    @property
    def min_center_distance(self):
        return keras.ops.min(self.fn.compute_center_distances())

    @property
    def max_center_distance(self):
        return keras.ops.max(self.fn.compute_center_distances())

    def on_train_batch_begin(self, batch, logs=None):
        self.fn.clear_next_centers()

    def on_train_batch_end(self, batch, logs=None):
        self.fn.update_centers()


class CenterBasedLoss(DistanceBasedLoss):
    '''
    Base class for center-based loss functions. Maintains the centers so subclasses only have to implement
    the loss calculation.
    '''

    def __init__(self, num_classes, embedding_dim, alpha=0.01, margin=0, center_movement=False,
                 center_update_movement_delay=0, distance="cosine"):
        super().__init__(distance)
        self.num_classes = num_classes
        self.embedding_dim = embedding_dim
        self.alpha = alpha
        self.center_movement = center_movement
        self.center_update_movement_delay = center_update_movement_delay
        self.centers = keras.Variable(
            CenterBasedLoss.equidistant_centers(num_classes, embedding_dim),
            dtype="float32",
            trainable=False,
            name="centers"
        )
        self.next_centers = keras.Variable(
            CenterBasedLoss.equidistant_centers(num_classes, embedding_dim),
            dtype="float32",
            trainable=False,
            name="centers"
        )
        self.ctr_margin = margin

    def __call__(self, labels, embeddings, axis=-1, training=False):
        if training:
            assert keras.ops.min(keras.ops.cast(labels, dtype="int32")) == 0, "Labels must be 0-based indexing"

        # ✅ Convert labels from 1-based to 0-based indexing
        # NOTE: We do this in the Custom Model Wrapper now instead of doing it here so it applies to all loss functions.
        labels = keras.ops.cast(labels, dtype="int32")
        loss = self.center_loss(labels, embeddings)

        next_centers = self.compute_new_centers(labels, embeddings)
        self.next_centers.assign(next_centers)
        min_center_dist, _ = self.compute_center_distances(centers=next_centers)
        loss += keras.ops.maximum(2 * self.ctr_margin - min_center_dist,
                                  0)  # Keep centers at least 1xmargin apart -- still allows overlap but should prevent collapsing.

        return loss

    def clear_next_centers(self):
        self.next_centers.assign(self.centers)

    def update_centers(self):
        if keras.backend.backend() == "tensorflow":
            self.update_centers_tf()
        elif keras.backend.backend() == "torch":
            self.update_centers_torch()
        else:
            raise ValueError("Only TensorFlow backend is supported for this function.")

    def update_centers_tf(self):
        replica_context = tf.distribute.get_replica_context()
        if self.center_movement:
            new_centers = self.next_centers
            if replica_context is not None:
                def merge_fn(strategy, _new_centers):
                    '''
                    Runs in the Per-Replica context. Both replicas have identical values so use mean-reduction to avoid
                    the exploding weights.

                    :param strategy:
                    :param _new_centers:
                    :return:
                    '''
                    mean_ctrs = strategy.reduce(tf.distribute.ReduceOp.MEAN, _new_centers, axis=None)
                    self.centers.assign(mean_ctrs)
                    return mean_ctrs

                replica_context.merge_call(merge_fn, args=(new_centers,))
            else:
                self.centers.assign(new_centers)

    def update_centers_torch(self):
        if self.center_movement:
            new_centers = self.next_centers
            if dist.is_initialized():
                dist.all_reduce(new_centers, op=dist.ReduceOp.MEAN)
                self.centers.assign(new_centers)
            else:
                self.centers.assign(new_centers)

    @abstractmethod
    def center_loss(self, labels, embeddings):
        pass

    @staticmethod
    def equidistant_centers(n: int, d: int) -> keras.KerasTensor:
        """
        Returns an (n x d) Tensor of n points in d-dimensional space,
        placed so that all pairwise distances are equal on the unit sphere
        (i.e., they form a regular simplex embedded in R^d).

        Constraints:
          - n <= d + 1
            (Cannot have n > d+1 equidistant points in d-dim space.)

        Each row is one center (L2-normalized).
        """
        if n > d + 1:
            raise ValueError(f"Cannot place {n} equidistant points in {d}-dim space; the maximum is n = d+1.")

        # Create an (n x n) identity matrix and mean-center its rows
        E = keras.ops.eye(n, dtype="float32")
        c = keras.ops.mean(E, axis=0, keepdims=True)  # centroid of rows, shape: [1, n]
        V = E - c  # shape: [n, n], sum of rows = 0

        # SVD decomposition
        s, u, v = keras.ops.svd(V, full_matrices=False)

        # Ensure `u` is a 2D tensor if it has been flattened
        u_shape = keras.ops.shape(u)

        # Ensure `u` is a 2D tensor if it has been flattened
        if len(u_shape) == 1:  # If `u` is 1D, reshape to (n, 1)
            u = keras.ops.reshape(u, [n, 1])

        # Construct diagonal matrix from singular values
        s_diag = keras.ops.diag(s[: (n - 1)])

        # Compute M (n x (n-1))
        M = keras.ops.matmul(u[:, : (n - 1)], s_diag)  # shape: [n, (n-1)]

        # If d > (n-1), pad with zeros to match the embedding dimension
        pad_amount = d - (n - 1)
        out = keras.ops.pad(M, pad_width=pad_amount, mode="constant",
                            constant_values=0.0)  # pad columns

        # Normalize row-wise so points lie on the unit sphere
        out = out / keras.ops.norm(out, ord=2, axis=-1, keepdims=False)

        return out

    @staticmethod
    def initialize_orthogonal_centers(num_classes, embedding_dim):
        """Generates `num_classes` orthogonal unit vectors in `embedding_dim` space."""
        random_matrix = keras.random.normal([embedding_dim, embedding_dim])  # Square matrix
        q, _ = keras.ops.qr(random_matrix)  # QR decomposition ensures orthogonality
        orthogonal_vectors = q[:num_classes]
        return keras.ops.norm(orthogonal_vectors, ord=2, axis=1)  # Ensure unit norm

    def compute_new_centers(self, labels, embeddings):
        # ✅ Get unique labels and their counts in the batch
        unique_labels, _, counts = ops.unique_with_counts(labels)

        unique_labels = keras.ops.cast(unique_labels, dtype="int32")
        counts = keras.ops.cast(counts, dtype="float32") + 1e-6

        # ✅ Compute the sum of embeddings per class
        mask = keras.ops.cast(
            keras.ops.equal(keras.ops.expand_dims(labels, 1), keras.ops.expand_dims(unique_labels, 0)), dtype="float32")
        sum_embeddings = keras.ops.matmul(keras.ops.transpose(mask), embeddings)

        # ✅ Compute mean embeddings per class
        mean_embeddings = sum_embeddings / keras.ops.expand_dims(counts, 1)

        # ✅ Gather previous centers
        prev_centers = keras.ops.take(self.centers, unique_labels)

        # ✅ Update rule: C_c ← C_c + α * (mean_x - C_c)
        new_centers = prev_centers + self.alpha * (mean_embeddings - prev_centers)
        new_centers = keras.ops.norm(new_centers, ord=2, axis=1)

        # ✅ Scatter the updated centers back to the full centers tensor
        updated_centers = keras.ops.slice_update(
            self.centers,
            keras.ops.expand_dims(unique_labels, axis=1),
            new_centers
        )

        return updated_centers

    def compute_center_distances(self, centers=None):
        if centers is None:
            centers = self.centers

        """Compute the minimum and maximum Euclidean distances between class centers."""
        center_distances = self.dist(
            keras.ops.expand_dims(self.centers, axis=1),
            keras.ops.expand_dims(self.centers, axis=0),
        )
        # self-distances along the diagnoal will all be 0, so just take the max...
        max_dist = keras.ops.max(center_distances)  # Farthest center pair
        center_distances += keras.ops.eye(keras.ops.shape(self.centers)[0]) * 1e6
        min_dist = keras.ops.min(center_distances)  # Farthest center pair

        return min_dist, max_dist

    @property
    def current_centers(self):
        return self.centers

    @tf.function
    def nan_or_inf_check(self, x, tracer):
        assert (not keras.ops.any(keras.ops.isnan(x)))


class CenterTripletLoss(CenterBasedLoss):
    def __init__(self, num_classes, embedding_dim, square_distances=False, margin: float = 0.1, alpha=0.01,
                 center_movement=False):
        CenterBasedLoss.__init__(self,
                                 num_classes=num_classes,
                                 embedding_dim=embedding_dim,
                                 alpha=alpha,
                                 center_movement=center_movement,
                                 margin=margin)
        self.square_distances = square_distances
        self.margin = margin

    @staticmethod
    def weighted_loss(losses, gamma=1.5, epsilon=1e-6):
        # Raise loss to a power (gamma) to emphasize higher-loss samples
        weights = keras.ops.power(losses + epsilon, gamma)

        # Normalize weights so that they sum to 1
        weight_sum = keras.ops.sum(weights)
        weights = keras.ops.divide_no_nan(weights, weight_sum)

        # Compute weighted sum of losses
        return keras.ops.sum(weights * losses)

    def center_loss(self, labels, embeddings):
        positive_centers = keras.ops.take(self.centers, labels)

        # Shape: (batch_size, embedding_dim) ,,, distance_to_positive_center[i] is the distance to
        #   sample i's positive center.
        dist_to_positive_center = self.dist(embeddings, positive_centers)

        # Compute nearest negative center
        expanded_embeddings = keras.ops.expand_dims(embeddings, axis=1)  # Shape: (batch_size, 1, embedding_dim)
        expanded_centers = keras.ops.expand_dims(self.centers, axis=0)  # Shape: (1, num_classes, embedding_dim)

        # Shape: (batch_size, num_classes). dist_to_all_centers[i][j] is the distance from anchor i to center j
        dist_to_all_centers = self.dist(expanded_embeddings, expanded_centers)

        # Set distance to positive center to some obscene high value...
        mask = keras.ops.one_hot(labels, self.num_classes, dtype="int32")
        dist_to_all_centers = keras.ops.where(mask == 1, np.inf, dist_to_all_centers)

        # Find the nearest center...
        dist_to_nearest_negative_center = keras.ops.min(dist_to_all_centers, axis=1)  # (batch_size,)

        # Triplet-Center Loss computation
        loss = keras.ops.maximum(dist_to_positive_center + self.margin - dist_to_nearest_negative_center, 0)

        return self.weighted_loss(loss)


class CenterLoss(CenterBasedLoss):
    def __init__(self, num_classes, embedding_dim, square_distances=False, alpha=0.5):
        super().__init__(self, num_classes, embedding_dim, alpha=alpha, distance="euclidean")
        self.square_distances = square_distances

    def center_loss(self, labels, embeddings):
        """Compute center loss using Euclidean distance."""
        labels = keras.ops.cast(keras.ops.squeeze(labels), dtype="int32")
        centers_batch = keras.ops.take(self.centers, labels)

        # Compute distance instead of squared distance
        loss = keras.ops.mean(self.dist(embeddings, centers_batch))

        return loss
