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


class DistanceBasedLoss:
    def __init__(self, distance: str):
        self.distance = distance.lower()
        self.cosine_distance = self.distance == "cosine"

        if self.distance not in ["euclidean", "cosine"]:
            raise ValueError(f"Invalid distance: {self.distance}")

    def dist(self, x, y):
        if self.cosine_distance:
            return DistanceBasedLoss.cos_dist(x, y)
        else:
            return keras.ops.norm(x - y, axis=-1)

    def pairwise_dist(self, embeddings):
        if self.cosine_distance:
            return DistanceBasedLoss.pairwise_cosine_distances(embeddings)
        else:
            return DistanceBasedLoss.pairwise_euclidean_distances(embeddings)

    @staticmethod
    def cos_dist(x, y):
        """Computes cosine distance: 1 - cosine similarity"""
        return 1 - keras.ops.sum(x * y, axis=-1)  # Equivalent to 1 - cos(θ)

    @staticmethod
    def pairwise_cosine_distances(embeddings):
        """
        Computes pairwise cosine distances between embeddings.

        Args:
            embeddings: Tensor of shape [batch, embedding_dim]

        Returns:
            cosine_distance_matrix: Tensor of shape [batch, batch] with pairwise cosine distances
        """
        # Normalize embeddings to unit length (L2 normalization)
        # embeddings = keras.ops.norm(embeddings, ord=2, axis=1)

        # Compute cosine similarity (dot product of normalized embeddings)
        cosine_similarity = keras.ops.matmul(embeddings, keras.ops.transpose(embeddings))

        # Convert cosine similarity to cosine distance
        cosine_distance = 1.0 - cosine_similarity

        return cosine_distance

    @staticmethod
    def pairwise_euclidean_distances(embeddings):
        """
        Computes pairwise Euclidean distances between embeddings.

        Args:
            embeddings: Tensor of shape [batch, embedding_dim]

        Returns:
            distance_matrix: Tensor of shape [batch, batch] with pairwise distances
        """
        # Compute squared norms for each embedding (shape: [batch, 1])
        squared_norms = keras.ops.sum(keras.ops.square(embeddings), axis=1, keepdims=True)

        # Compute pairwise squared Euclidean distance using broadcasting:
        # ||a - b||^2 = ||a||^2 - 2 * a.b + ||b||^2
        two_a_b = keras.ops.multiply(2, keras.ops.matmul(embeddings, keras.ops.transpose(embeddings)))
        b_square = keras.ops.matmul(embeddings, keras.ops.transpose(embeddings))
        distance_matrix = keras.ops.subtract(squared_norms, keras.ops.add(two_a_b, b_square))

        # Ensure numerical stability (remove small negative values)
        distance_matrix = keras.ops.maximum(distance_matrix, keras.ops.zeros_like(distance_matrix))

        # Take square root to get actual Euclidean distances
        distance_matrix = keras.ops.sqrt(distance_matrix)

        return distance_matrix
