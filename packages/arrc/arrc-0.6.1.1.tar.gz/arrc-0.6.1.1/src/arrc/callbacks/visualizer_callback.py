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

from abc import abstractmethod

import keras
import matplotlib

# matplotlib.use('Agg')
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import traceback
import os

import numpy as np

from arrc.losses import CenterLoss, CenterTripletLoss, CenterTripletLossWrapper


class AbstractVisualizerCallback(keras.callbacks.Callback):
    def __init__(self,
                 model_for_embeddings,  # your trained model or sub-model that outputs embeddings
                 validation_dataset,
                 validation_steps=None,
                 log_dir='./logs_embeddings',
                 frequency=1,  # run every 'frequency' epochs
                 random_state=42,
                 center_loss_fn: CenterLoss | CenterTripletLoss | CenterTripletLossWrapper = None,
                 embedding_len=128,
                 num_classes=2,
                 class_labels = None):
        super().__init__()
        self.model_for_embeddings = model_for_embeddings
        self.validation_dataset = validation_dataset
        self.validation_steps = validation_steps
        self.log_dir = log_dir
        self.frequency = frequency
        self.random_state = random_state
        self.center_loss_fn = center_loss_fn
        self.embedding_len = embedding_len
        self.num_classes = num_classes
        self.backend = keras.backend.backend()

        if class_labels is None:
            class_labels = [f"Class {i}" for i in range(num_classes)]
        self.class_labels = class_labels

        os.makedirs(self.log_dir, exist_ok=True)

    @abstractmethod
    def fit_transform(self, embeddings):
        pass

    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % self.frequency == 0:
            self.plot_embeddings(epoch)

    def plot_embeddings(self, epoch):
        labels = []
        embeddings = []

        val_itr = iter(self.validation_dataset)
        for i in range(self.validation_steps):
            try:
                x, y_true = None, None
                batch = next(val_itr)

                if self.backend == 'tensorflow':
                    y_true, x = batch
                elif self.backend == 'torch':
                    x, y_true  = batch

                labels.extend(y_true.numpy())  # Ensure NumPy conversion

                result = self.model_for_embeddings(x, training=False)
                if isinstance(result, list) or isinstance(result, tuple):
                    result = result[0]

                embeddings.extend(result.detach().cpu().numpy())
            except StopIteration:
                pass

        labels = np.array(labels)
        embeddings = np.array(embeddings)

        # Note -- we fixed the model so it still returns l2-normalized embeddings.
        # embeddings = tf.nn.l2_normalize(embeddings, -1)
        embedding_len = len(embeddings)
        if self.center_loss_fn is not None:
            centers = np.array(self.center_loss_fn.current_centers.numpy())  # Convert to NumPy
            embeddings = np.vstack([embeddings, centers])

        num_classes = self.num_classes  # max(labels)  # Adjust for zero-based indexing
        cmap = plt.cm.get_cmap("tab20b", num_classes)  # Distinct colors per class

        # 🚀 Apply UMAP to reduce dimensions to 3D
        try:
            emb_3d = self.fit_transform(embeddings)
            emb_transformed = emb_3d[:embedding_len]  # UMAP-transformed embeddings
            centers_transformed = emb_3d[embedding_len:]  # UMAP-transformed centers

            colors = [cmap(label) for label in labels]  # Colors for embeddings
            center_colors = [cmap(i) for i in range(num_classes)]  # Colors for centers

            # 🎨 3D Plot
            fig = plt.figure(figsize=(12, 10))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(emb_transformed[:, 0], emb_transformed[:, 1], emb_transformed[:, 2],
                       c=colors, alpha=0.7, label="Data Points")

            if self.center_loss_fn is not None:
                ax.scatter(centers_transformed[:, 0], centers_transformed[:, 1], centers_transformed[:, 2],
                           c=center_colors, edgecolors='black', marker='X', s=200, label="Class Centers")

            # 🏷️ Custom Legend
            legend_handles = [
                mpatches.Patch(color=center_colors[i], label=self.class_labels[i]) for i in range(num_classes)
            ]
            plt.legend(handles=legend_handles, title="Class Labels")

            plt.title(f"Embeddings at Epoch {epoch + 1}")

            # 📂 Save Figure
            plot_path = os.path.join(self.log_dir, f"epoch_{epoch + 1}.png")
            plt.savefig(plot_path, dpi=600)
            plt.close()
        except Exception as e:
            print(f"WARNING: Exception occurred plotting embeddings at epoch {epoch + 1}: {e}")
            traceback.print_exc()  # Print the full traceback
            raise e
