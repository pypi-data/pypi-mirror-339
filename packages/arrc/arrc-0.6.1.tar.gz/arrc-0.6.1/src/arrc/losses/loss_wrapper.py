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
from keras.src.losses.loss import squeeze_or_expand_to_same_rank
from keras.src.saving import serialization_lib


class LossFunctionWrapper(keras.losses.Loss):
    def __init__(
            self, fn, reduction="mean", name=None, **kwargs
    ):
        super().__init__(reduction=reduction, name=name)
        self.fn = fn
        self._fn_kwargs = kwargs

    @property
    def fn_kwargs(self):
        return self._fn_kwargs

    @fn_kwargs.setter
    def fn_kwargs(self, fn_kwargs):
        self._fn_kwargs = fn_kwargs

    def call(self, y_true, y_pred):
        y_true, y_pred = squeeze_or_expand_to_same_rank(y_true, y_pred)
        return self.fn(y_true, y_pred, **self._fn_kwargs)

    def get_config(self):
        base_config = super().get_config()
        config = {"fn": serialization_lib.serialize_keras_object(self.fn)}
        config.update(serialization_lib.serialize_keras_object(self._fn_kwargs))
        return {**base_config, **config}

    @classmethod
    def from_config(cls, config):
        if "fn" in config:
            config = serialization_lib.deserialize_keras_object(config)
        return cls(**config)
