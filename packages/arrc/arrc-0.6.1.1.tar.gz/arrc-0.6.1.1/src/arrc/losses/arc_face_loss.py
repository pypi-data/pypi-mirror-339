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

from arrc.losses.loss_wrapper import LossFunctionWrapper


def arcface_loss(y_true, cosine_logits, margin=0.5, scale=30.0):
    """
    y_true: Sparse integer class labels (batch_size,)
    cosine_logits: Cosine similarity logits (batch_size, num_classes)
    Returns: Softmax cross-entropy loss with ArcFace margin
    """
    # Get one-hot labels
    y_true = keras.ops.cast(y_true, dtype="int32")
    y_true_one_hot = keras.ops.one_hot(y_true, depth=keras.ops.shape(cosine_logits)[-1])

    # Compute angles (acos of cosine similarity)
    theta = keras.ops.arccos(keras.ops.clip(cosine_logits, -1.0, 1.0))

    # Apply margin to target class
    target_logits = keras.ops.cos(theta + margin)

    # Replace original logits for the target class only
    modified_logits = (y_true_one_hot * target_logits) + ((1 - y_true_one_hot) * cosine_logits)

    # Scale before softmax
    scaled_logits = modified_logits * scale

    # Compute cross-entropy loss
    # @TODO: check whether from_logits is supposed to be True or False here ...
    #  https://keras.io/guides/migrating_to_keras_3/
    # loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y_true, logits=scaled_logits)
    loss = keras.ops.sparse_categorical_crossentropy(y_true=y_true, output=keras.ops.shape(y_true),
                                                     from_logits=True, dtype=cosine_logits.dtype)
    return keras.ops.mean(loss)


class ArcFaceLoss(LossFunctionWrapper):
    def __init__(self, margin=0.3, scale=10.0, reduction="mean", name="arcface_loss"):
        super().__init__(fn=arcface_loss, reduction=reduction, name=name, margin=margin, scale=scale)
