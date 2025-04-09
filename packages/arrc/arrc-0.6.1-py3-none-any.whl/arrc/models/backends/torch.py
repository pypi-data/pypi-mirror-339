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
import torch
import torch.distributed as dist
import torch.nn as nn


class TorchTrainer:
    def __init__(self):
        pass

    @staticmethod
    def unwrap_model(model):
        """Unwraps a model from DataParallel or DistributedDataParallel."""
        if isinstance(model, (nn.DataParallel, nn.parallel.DistributedDataParallel)):
            return model.module
        return model

    def forward_pass(self, x, *args, **kwargs):
        self.train()
        out = self(x, training=True)

        unwrapped_model = TorchTrainer.unwrap_model(self)
        if unwrapped_model.classification_enabled:
            embeddings, logits, softmax_output = out
        else:
            embeddings, logits, softmax_output = out, None, None

        return embeddings, logits, softmax_output

    def backward_pass(self, loss_value):
        unwrapped_model = TorchTrainer.unwrap_model(self)
        optimizer = unwrapped_model.optimizer

        if isinstance(optimizer, torch.optim.Optimizer):
            optimizer.zero_grad()  # torch.optim.Optimizer tracks the model's weights + grads.
            loss_value.backward()  # run the back pass
            optimizer.step()       # apply gradients
        elif isinstance(optimizer, keras.Optimizer):
            self.zero_grad()
            trainable_variables = [v for v in self.trainable_weights]
            loss_value.backward()  # run the backward pass

            # apply gradients
            gradients = [v.value.grad for v in trainable_variables]
            with torch.no_grad():
                optimizer.apply(gradients, trainable_variables)

    @staticmethod
    def get_rank():
        return torch.distributed.get_rank() if torch.distributed.is_initialized() else 0

    def compute_loss(self, embeddings, logits, softmax_output, labels):
        loss_value = 0
        unwrapped_model = TorchTrainer.unwrap_model(self)
        if "embedding" in unwrapped_model.loss_fn_map:
            weight = unwrapped_model.loss_fn_weights["embedding"]
            loss_value = loss_value + weight * unwrapped_model.loss_fn_map["embedding"](y_true=labels, y_pred=embeddings)

        if "logits" in unwrapped_model.loss_fn_map and logits is not None:
            weight = unwrapped_model.loss_fn_weights["logits"]
            loss_value = loss_value + weight * unwrapped_model.loss_fn_map["logits"](y_true=labels, y_pred=logits)

        if "classifications" in unwrapped_model.loss_fn_map and softmax_output is not None:
            weight = unwrapped_model.loss_fn_weights["classifications"]
            loss_value = loss_value + weight * unwrapped_model.loss_fn_map["classifications"](y_true=labels, y_pred=softmax_output)

        return loss_value

    def get_synced_metrics(self):
        synced_metric_results = {}
        world_size = 1 if not torch.distributed.is_initialized() else torch.distributed.get_world_size()

        for metric in TorchTrainer.unwrap_model(self).metrics:
            metric_tensor = metric.result()
            if world_size > 1:

                torch.distributed.all_reduce(metric_tensor, op=torch.distributed.ReduceOp.SUM)
            synced_metric_results[metric.name] = metric_tensor / world_size

        return synced_metric_results

    def on_train_begin(self, *args, **kwargs):
        optimizer = kwargs.get("optimizer", None)
        unwrapped_model = TorchTrainer.unwrap_model(self)
        unwrapped_model.optimizer = optimizer

    def on_epoch_begin(self, epoch, *args, **kwargs):
        sampler = None
        dataloader = kwargs.get("dataloader", None)
        validation_dataloader = kwargs.get("validation_dataloader", None)

        if isinstance(dataloader.sampler, torch.utils.data.distributed.DistributedSampler):
            sampler = dataloader.sampler
            sampler.set_epoch(epoch) if sampler is not None else None

        if validation_dataloader is not None and isinstance(validation_dataloader.sampler, torch.utils.data.distributed.DistributedSampler):
            validation_sampler = validation_dataloader.sampler
            validation_sampler.set_epoch(epoch) if sampler is not None else None

        unwrapped_model = TorchTrainer.unwrap_model(self)
        unwrapped_model.reset_metrics()

    def on_train_batch_begin(self, step, *args, **kwargs):
        self.train()
        data = kwargs.get("data", None)
        device = kwargs.get("device", f"cuda:{torch.cuda.current_device()}")
        if data is None:
            raise ValueError("Data is required for training.")
        input, targets = data
        input.to(device)
        targets.to(device)

    def on_train_batch_end(self, step, data, *args, **kwargs):
        pass

    def on_test_batch_begin(self, step, data, *args, **kwargs):
        self.eval()

    def on_test_batch_end(self, step, data, *args, **kwargs):
        pass

    def on_epoch_end(self, epoch, *args, **kwargs):
        unwrapped_model = TorchTrainer.unwrap_model(self)
        unwrapped_model.reset_metrics()

    def on_train_end(self, *args, **kwargs):
        pass
