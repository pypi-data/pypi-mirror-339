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

from .arc_face_loss import ArcFaceLoss, arcface_loss
from .center_loss import CenterTripletLossWrapper, CenterTripletLoss, CenterLoss
from .combined_loss import CombinedLossWrapper, CombinedLoss
from .contrastive_loss import ContrastiveLossWrapper, ContrastiveLoss
from .distance_loss import DistanceBasedLoss
from .triplet_loss import TripletLossWrapper, TripletLoss
