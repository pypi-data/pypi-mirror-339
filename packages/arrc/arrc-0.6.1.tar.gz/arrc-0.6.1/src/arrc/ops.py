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
import numpy as np


def l2_normalize(x, axis=-1, keepdims=False):
    return keras.ops.norm(x, ord=2, axis=axis, keepdims=keepdims)


def to_tensor(x):
    return keras.ops.convert_to_tensor(x)


def shape(x):
    return keras.ops.shape(
        to_tensor(x)
    )


def boolean_mask(tensor, mask, name="boolean_mask", axis=None):
    """Apply boolean mask to tensor. This is a re-implementation of `tf.boolean_mask`
    in Keras3.

    Numpy equivalent is `tensor[mask]`.

    In general, `0 < dim(mask) = K <= dim(tensor)`, and `mask`'s shape must match
    the first K dimensions of `tensor`'s shape.  We then have:
      `boolean_mask(tensor, mask)[i, j1,...,jd] = tensor[i1,...,iK,j1,...,jd]`
    where `(i1,...,iK)` is the ith `True` entry of `mask` (row-major order).
    The `axis` could be used with `mask` to indicate the axis to mask from.
    In that case, `axis + dim(mask) <= dim(tensor)` and `mask`'s shape must match
    the first `axis + dim(mask)` dimensions of `tensor`'s shape.

    See also: `tf.ragged.boolean_mask`, which can be applied to both dense and
    ragged tensors, and can be used if you need to preserve the masked dimensions
    of `tensor` (rather than flattening them, as `tf.boolean_mask` does).

    Examples:

    ```python
    # 1-D example
    tensor = [0, 1, 2, 3]
    mask = np.array([True, False, True, False])
    tf.boolean_mask(tensor, mask)  # [0, 2]

    # 2-D example
    tensor = [[1, 2], [3, 4], [5, 6]]
    mask = np.array([True, False, True])
    tf.boolean_mask(tensor, mask)  # [[1, 2], [5, 6]]
    ```

    Args:
      tensor:  N-D Tensor.
      mask:  K-D boolean Tensor, K <= N and K must be known statically.
      name:  A name for this operation (optional).
      axis:  A 0-D int Tensor representing the axis in `tensor` to mask from. By
        default, axis is 0 which will mask from the first dimension. Otherwise K +
        axis <= N.

    Returns:
      (N-K+1)-dimensional tensor populated by entries in `tensor` corresponding
      to `True` values in `mask`.

    Raises:
      ValueError:  If shapes do not conform.
    """

    def _apply_mask_1d(reshaped_tensor, mask, axis=None):
        """Mask tensor along dimension 0 with a 1-D mask."""
        mask = keras.ops.cast(mask, dtype="int32")
        indices = keras.ops.squeeze(keras.ops.nonzero(mask))
        return keras.ops.take(reshaped_tensor, indices, axis=axis)

    tensor = keras.ops.convert_to_tensor(tensor)
    mask = keras.ops.convert_to_tensor(mask)

    shape_mask = keras.ops.shape(mask)
    ndims_mask = len(shape_mask)
    if ndims_mask == 0:
        raise ValueError("mask cannot be scalar.")
    if ndims_mask is None:
        raise ValueError(
            "Number of mask dimensions must be specified, even if some dimensions"
            " are None.  E.g. shape=[None] is ok, but shape=None is not.")

    axis = 0 if axis is None else axis

    leading_size = keras.ops.prod(keras.ops.shape(tensor)[axis:axis + ndims_mask], [0])
    tensor = keras.ops.reshape(
        tensor,
        keras.ops.cast(
            keras.ops.concatenate([
                to_tensor(shape(tensor)[:axis]),
                to_tensor([leading_size]),
                to_tensor(shape(tensor)[axis + ndims_mask:])
            ], 0),
            dtype="int32"))

    mask = keras.ops.reshape(mask, [-1])
    return _apply_mask_1d(tensor, mask, axis)


def unique_with_counts(tensor):
    """Keras 3 multi-backend-compatible implementation of tf.unique_with_counts.

    Args:
        tensor: A 1D NumPy array or Keras tensor.

    Returns:
        A tuple of (unique_values, indices, counts), where:
            - unique_values: The unique elements in the input tensor.
            - indices: The indices in the unique array corresponding to each element in tensor.
            - counts: The count of each unique element.
    """
    tensor = keras.ops.convert_to_tensor(tensor)

    # Convert tensor to NumPy for unique processing
    tensor_np = np.array(tensor)
    unique_values, indices, counts = np.unique(tensor_np, return_inverse=True, return_counts=True)

    # Convert results back to Keras tensors
    unique_values = keras.ops.convert_to_tensor(unique_values)
    indices = keras.ops.convert_to_tensor(indices)
    counts = keras.ops.convert_to_tensor(counts)

    return unique_values, indices, counts
