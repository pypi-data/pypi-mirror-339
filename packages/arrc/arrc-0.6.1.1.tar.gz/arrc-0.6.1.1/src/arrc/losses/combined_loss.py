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


from typing import Callable

import numpy as np

from .loss_wrapper import LossFunctionWrapper


class CombinedLossWrapper(LossFunctionWrapper):
    def __init__(self, loss_functions, loss_weights=None, reduction="sum_over_batch_size"):
        super().__init__(
            fn=CombinedLoss(loss_functions, loss_weights),
            reduction=reduction,
            name="combined_loss",
        )


class CombinedLoss(Callable):
    def __init__(self, loss_functions, loss_weights=None):
        '''
        A wrapper loss function that takes a list of loss functions and a list of weights used to combine them.

        :param loss_functions: A list of loss functions to invoke
        :param loss_weights: The weights to apply to each loss function. If none, defaults to np.ones_like(loss_functions).
        '''
        if loss_weights is None:
            loss_weights = np.ones_like(loss_functions)

        if len(loss_weights) != len(loss_functions):
            raise ValueError("You must provide a weight for each loss function.")

        for loss in loss_functions:
            if not isinstance(loss, LossFunctionWrapper):
                raise TypeError("Loss functions must be a LossFunctionWrapper object.")

        self.loss_functions = loss_functions
        self.loss_weights = loss_weights

    def __call__(self, y_true, y_pred, **kwargs):
        '''
        Calls each loss function and reduces their results to a single value based on the given weights.

            total_loss = sum(loss_function[i](y_true, y_pred) * loss_weights[i]) for all loss functions.

        :param y_true:
        :param y_pred:
        :return:
        '''
        loss = 0

        for loss_fn, weight in zip(self.loss_functions, self.loss_weights):
            loss_fn.fn_kwargs = kwargs
            loss += weight * loss_fn(y_true, y_pred)

        return loss
