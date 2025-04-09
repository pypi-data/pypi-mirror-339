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

import torch
import torch.distributed as dist
import torch.nn as nn
import tensorflow as tf

class TensorflowTrainer:
    def __init__(self):
        pass

    def forward_pass(self, x, *args, **kwargs):
        with (tf.GradientTape() as tape):
            x = self.call(x, training=True)  # Logits for this minibatch

            # outputs, softmax_output, logits
            if self.classification_enabled:
                embeddings, logits, softmax_output = x
            else:
                embeddings, logits, softmax_output = x, None, None

        return embeddings, logits, softmax_output

    def backward_pass(self, loss_value, optimizer):
        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)
        optimizer.apply(gradients, trainable_vars)

    @staticmethod
    def get_rank():
        return tf.distribute.get_replica_context().replica_id_in_sync_group if tf.distribute.has_strategy() else 0

    def compute_loss(self, embeddings, logits, softmax_output, labels):
        with (tf.GradientTape() as tape):
            loss_value = 0
            if "embeddings" in self.loss_fn_map:
                loss_value += self.loss_fn_map["embeddings"](y_true=labels, y_pred=embeddings)
            if "logits" in self.loss_fn_map and logits is not None:
                loss_value += self.loss_fn_map["logits"](y_true=labels, y_pred=logits)
            if "classifications" in self.loss_fn_map and softmax_output is not None:
                loss_value += self.loss_fn_map["classifications"](y_true=labels, y_pred=softmax_output)
        return loss_value

    def on_epoch_begin(self, epoch, *args, **kwargs):
        for metric in self.metrics:
            metric.reset_state()

    def on_train_begin(self, *args, **kwargs):
        pass

    def on_train_batch_begin(self, step, data, *args, **kwargs):
        pass

    def on_train_batch_end(self, step, data, *args, **kwargs):
        pass

    def on_test_batch_begin(self, step, data, *args, **kwargs):
        pass

    def on_test_batch_end(self, step, data, *args, **kwargs):
        pass

    def on_epoch_end(self, epoch, *args, **kwargs):
        pass

    def on_train_end(self, *args, **kwargs):
        pass