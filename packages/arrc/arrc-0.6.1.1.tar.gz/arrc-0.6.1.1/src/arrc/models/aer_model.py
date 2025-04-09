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

import os

import keras
from arrc.layers import ArcFace, MetricEmbedding
from hatch.cli import self

keras_backend = os.environ.get('KERAS_BACKEND', keras.backend.backend())
if keras_backend == 'torch':
    from arrc.models.backends.torch import TorchTrainer as BaseARRCModel
elif keras_backend == 'tensorflow':
    from arrc.models.backends.tensorflow import TensorflowTrainer as BaseARRCModel
else:
    raise ValueError(f"Unsupported KERAS_BACKEND: {keras_backend}")

@keras.saving.register_keras_serializable()
class ARRCModel(BaseARRCModel, keras.Model):
    def __init__(self, num_classes: int = 2, classification_loss_weight=0,
                 embedding_dim=32, embedding_metrics=None, logits_metrics=None, classification_metrics=None,
                 *args, **kwargs):
        print("Initializing ARRCModel")
        keras.Model.__init__(self,*args, **kwargs)
        BaseARRCModel.__init__(self)

        self.classification_enabled = num_classes is not None and num_classes > 0

        self.args = args
        self.kwargs = kwargs

        if num_classes < 1:
            num_classes = 1

        if embedding_metrics is None:
            embedding_metrics = []

        if classification_metrics is None:
            classification_metrics = []

        if logits_metrics is None:
            logits_metrics = []

        self._embedding_dim = embedding_dim
        self._num_classes = num_classes
        self._classification_loss_weight = classification_loss_weight

        self._embedding_metrics = embedding_metrics
        self._classification_metrics = classification_metrics
        self._logits_metrics = logits_metrics

        # For tracking total loss
        self.loss_tracker = keras.metrics.Mean(name="loss", dtype="float64")
        self.optimizer = None
        self.built = True
        self.stop_training = False


    @staticmethod
    def BuildARRCModel(inputs,
                       embedding_outputs,
                       num_classes: int = 2,
                       num_fc_layers: int = 3,
                       classification_activation = None,
                       fc_dropout_rate: int = 0.5,
                       distance_metric="euclidean",
                       arcface=False,
                       name="arrc_model",
                       *args,
                       **kwargs):
        classification_enabled = num_classes is not None and num_classes > 0

        if classification_enabled:
            if classification_activation is None:
                classification_activation = "softmax" if num_classes > 1 else "sigmoid"

            classification_head = embedding_outputs
            for i in range(num_fc_layers):
                n = num_fc_layers - i
                classification_head = keras.layers.Dense(
                    units=embedding_outputs.shape[-1] // (i+1),
                    name=f"classification_head_{i}",
                    activation="relu"
                )(classification_head)
                classification_head = keras.layers.Dropout(rate=fc_dropout_rate)(classification_head)
                # classification_head = keras.layers.LayerNormalization()(classification_head)
                # classification_head = keras.layers.Activation('relu')(classification_head)

            if arcface:
                classifier_dense = ArcFace(num_classes, name="arcface_logits")(classification_head)
            else:
                classifier_dense = keras.layers.Dense(num_classes, name='logits')(classification_head)

            classifier = keras.layers.Activation(classification_activation,  name=f'{classification_activation}_activation')(classifier_dense)

            return ARRCModel(inputs=inputs,
                             outputs=[embedding_outputs, classifier_dense, classifier],
                             name=f"{name}_classifier",
                             embedding_dim=embedding_outputs.shape[-1],
                             num_classes=num_classes,
                             jit_compile=True,
                             *args,
                             **kwargs)
        else:
            embedding_outputs = MetricEmbedding(units=embedding_outputs.shape[-1], distance_metric=distance_metric, name="embedding")(embedding_outputs)
            return ARRCModel(inputs=inputs,
                             outputs=embedding_outputs,
                             embedding_dim=embedding_outputs.shape[-1],
                             name=f"{name}",
                             num_classes=num_classes,
                             jit_compile=True,
                             *args,
                             **kwargs)

    @staticmethod
    def BuildARRCLossMapsForModel(model, embedding_loss_fn=None, logits_loss_fn=None, classification_loss_fn=None,
                                  embedding_loss_wgt=1.0, logits_loss_wgt=1.0, classification_loss_wgt=1.0):
        loss_fns = {}
        loss_wgts = {}
        if embedding_loss_fn is not None:
            loss_fns["embedding"] = embedding_loss_fn
            loss_wgts["embedding"] = embedding_loss_wgt

        if model.is_classification_enabled and classification_loss_fn is not None:
            loss_fns["classifications"] = classification_loss_fn
            loss_wgts["classifications"] = classification_loss_wgt

        if model.is_classification_enabled and logits_loss_fn is not None:
            loss_fns["logits"] = logits_loss_fn
            loss_wgts["logits"] = logits_loss_wgt

        return loss_fns, loss_wgts

    @property
    def is_classification_enabled(self):
        return self.classification_enabled > 0

    @property
    def loss_fn_map(self):
        return self._loss_fn_map

    @loss_fn_map.setter
    def loss_fn_map(self, loss_fn_map):
        self._loss_fn_map = loss_fn_map
        if "embedding" in self._loss_fn_map:
            fn = self._loss_fn_map["embedding"]
            self.add_embedding_metric(
                keras.metrics.MeanMetricWrapper(name="embedding_loss", fn=fn))
        if "classifications" in self._loss_fn_map:
            fn = self._loss_fn_map["classifications"]
            self.add_classification_metric(
                keras.metrics.MeanMetricWrapper(name="classification_loss", fn=fn))
        if "logits" in self._loss_fn_map:
            fn = self._loss_fn_map["logits"]
            self.add_logits_metric(
                keras.metrics.MeanMetricWrapper(name="logits_loss", fn=fn))

    @property
    def loss_fn_weights(self):
        return self._loss_fn_wgts

    @loss_fn_weights.setter
    def loss_fn_weights(self, loss_fn_weights):
        self._loss_fn_wgts = loss_fn_weights

    @property
    def num_classes(self):
        return self._num_classes if self._num_classes is not None else 0

    @property
    def embedding_metrics(self):
        return self._embedding_metrics

    @property
    def classification_metrics(self):
        return self._classification_metrics

    @property
    def logits_metrics(self):
        return self._logits_metrics

    @property
    def metrics(self):
        return [self.loss_tracker] + self.embedding_metrics + self.classification_metrics + self.logits_metrics

    def add_embedding_metric(self, metric):
        try:
            self.embedding_metrics.extend(metric)
        except TypeError:
            self.embedding_metrics.append(metric)

    def add_classification_metric(self, metric):
        try:
            self.classification_metrics.extend(metric)
        except TypeError:
            self.classification_metrics.append(metric)

    def add_logits_metric(self, metric):
        try:
            self._logits_metrics.extend(metric)
        except TypeError:
            self._logits_metrics.append(metric)

    def call_metrics(self, labels, embeddings, logits, softmax_output):
        for metric in self.embedding_metrics:
            try:
                metric.update_state(y_true=labels, y_pred=embeddings)
            except Exception as e:
                raise e

        if self.classification_enabled and logits is not None:
            for metric in self.logits_metrics:
                metric.update_state(y_true=labels, y_pred=logits)

        if self.classification_enabled and softmax_output is not None:
            for metric in self.classification_metrics:
                metric.update_state(y_true=keras.ops.reshape(labels, (labels.shape[0],1)), y_pred=softmax_output)

    def reset_metrics(self):
        for m in self.metrics:
            m.reset_state()

    def train_step(self, data):
        x, y_true = data
        labels = keras.ops.cast(y_true, "int32")


        embeddings, logits, softmax_output = ARRCModel.forward_pass(self, x)
        if softmax_output is not None:
            softmax_output = keras.ops.where(keras.ops.isnan(softmax_output), 0.5, softmax_output)

        loss_value = ARRCModel.compute_loss(self, embeddings, logits, softmax_output, labels)
        ARRCModel.backward_pass(self, loss_value)

        # Update metrics
        unwrapped_model = ARRCModel.unwrap_model(self)  # Use only for property access - do not call this model
        unwrapped_model.loss_tracker.update_state(loss_value)
        unwrapped_model.call_metrics(labels, embeddings, logits, softmax_output)
        local_dict = ARRCModel.get_synced_metrics(self)

        return local_dict

    def test_step(self, data):
        x, y_true = data
        labels = keras.ops.cast(y_true, "int32")

        result = self(x, training=False)  # Logits for this minibatch

        unwrapped_model = ARRCModel.unwrap_model(self)  # Use only for property access - do not call this model
        if unwrapped_model.is_classification_enabled:
            embeddings, logits, softmax_output = result
            softmax_output = keras.ops.where(keras.ops.isnan(softmax_output), 0.5, softmax_output)
        else:
            embeddings, logits, softmax_output = result, None, None

        loss_value = ARRCModel.compute_loss(self, embeddings, logits, softmax_output, labels)

        unwrapped_model.loss_tracker.update_state(loss_value)
        unwrapped_model.call_metrics(labels, embeddings, logits, softmax_output)
        local_dict = ARRCModel.get_synced_metrics(self)

        return local_dict

    def arrc_fit(self, optimizer, scheduler, epochs, dataloader, validation_dataloader, steps_per_epoch=None, validation_steps=None, callbacks=None, verbose=1):
        if callbacks is None:
            callbacks = []

        if steps_per_epoch is None:
            steps_per_epoch = len(dataloader)

        if validation_steps is None and validation_dataloader is not None:
            validation_steps = len(validation_dataloader)

        training_logs = None

        if not isinstance(callbacks, keras.callbacks.CallbackList):
            callbacks = keras.callbacks.CallbackList(
                callbacks=callbacks,
                add_history=True,
                add_progbar=ARRCModel.get_rank() == 0,
                verbose=verbose,
                epochs=epochs,
                steps=len(dataloader),
                model=self,
            )

        ARRCModel.on_train_begin(self, optimizer=optimizer)
        callbacks.on_train_begin()

        for epoch in range(epochs):
            epoch_logs = {}

            ARRCModel.on_epoch_begin(self, epoch, dataloader=dataloader, validation_dataloader=validation_dataloader)
            callbacks.on_epoch_begin(epoch)
            train_iter = iter(dataloader)
            for step in range(steps_per_epoch):
                train_batch_data = next(train_iter)
                ARRCModel.on_train_batch_begin(self, step, data=train_batch_data)
                callbacks.on_train_batch_begin(batch=step)

                train_log = ARRCModel.train_step(self, train_batch_data)

                if hasattr(optimizer, 'learning_rate'):
                    train_log['lr'] = optimizer.learning_rate
                elif hasattr(optimizer, 'lr'):
                    train_log['lr'] = optimizer.lr
                elif keras.backend.backend() == 'torch' and hasattr(optimizer, 'param_groups') and len(optimizer.param_groups) > 0 and 'lr' in optimizer.param_groups[0]:
                    train_log['lr'] = optimizer.param_groups[0]['lr']
                    if scheduler is not None:
                        scheduler.step()


                callbacks.on_train_batch_end(batch=step, logs=train_log)
                ARRCModel.on_train_batch_end(self, step, train_batch_data)

                epoch_logs.update(train_log)

            ARRCModel.reset_metrics(ARRCModel.unwrap_model(self))

            if validation_dataloader is not None:
                validation_iter = iter(validation_dataloader)
                for step in range(validation_steps):
                    validation_batch_data = next(validation_iter)
                    ARRCModel.on_test_batch_begin(self, step, validation_batch_data)
                    callbacks.on_test_batch_begin(batch=step)

                    test_log = ARRCModel.test_step(self, validation_batch_data)
                    test_log = {f'val_{key}': val for key, val in test_log.items()}

                    callbacks.on_test_batch_end(batch=step, logs=test_log)
                    ARRCModel.on_test_batch_end(self, step, validation_batch_data)
                    epoch_logs.update(test_log)

            callbacks.on_epoch_end(epoch=epoch, logs=epoch_logs)
            ARRCModel.on_epoch_end(self, epoch)

            training_logs = epoch_logs

            if ARRCModel.unwrap_model(self).stop_training:
                break

        callbacks.on_train_end(logs=training_logs)
        ARRCModel.on_train_end(self)

    def get_config(self):
        config = super().get_config()
        config.update({
            "num_classes": self._num_classes,
            "embedding_dim": self._embedding_dim,
        })
        config.update(self.kwargs)
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)