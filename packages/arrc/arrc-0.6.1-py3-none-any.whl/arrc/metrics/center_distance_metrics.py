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


class CenterDistanceMetric(keras.metrics.Mean):
    def __init__(self, center_loss_fn=None, min_distance=True, **kwargs):
        super(CenterDistanceMetric, self).__init__(**kwargs)
        self.center_loss_fn = center_loss_fn
        self.min_distance = min_distance

    def update_state(self, *args, **kwargs):
        value = self.center_loss_fn.min_center_distance if self.min_distance else self.center_loss_fn.max_center_distance
        super(CenterDistanceMetric, self).update_state(value)


class MinCenterDistanceMetric(CenterDistanceMetric):
    def __init__(self, name="min_ctr_dist", **kwargs):
        super(MinCenterDistanceMetric, self).__init__(min_distance=True, name=name, **kwargs)


class MaxCenterDistanceMetric(CenterDistanceMetric):
    def __init__(self, name="max_ctr_dist", **kwargs):
        super(MaxCenterDistanceMetric, self).__init__(min_distance=False, name=name, **kwargs)
