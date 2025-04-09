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
import matplotlib

# matplotlib.use('Agg')  # Use non-interactive backend for saving plots
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.spatial.distance import pdist


class HistogramEmbeddingVisualizerCallback(keras.callbacks.Callback):
    """
    A Callback to compute embeddings from a model, analyze pairwise cosine distances, and render
    histograms to monitor their distribution after each specified epoch.

    Designed to evaluate the quality of embeddings derived from a model and track their distribution
    behavior during training, aiming to ensure desired separability characteristics.

    :ivar model_for_embeddings: The model or sub-model used to generate embeddings.
    :type model_for_embeddings: keras.models.Model

    :ivar validation_dataset: Dataset utilized for inference to generate embeddings.
    :type validation_dataset: tf.data.Dataset

    :ivar validation_steps: Number of steps to iterate over `validation_dataset` to extract embeddings.
    :type validation_steps: int, optional

    :ivar log_dir: Directory path where the generated histogram plots are stored.
    :type log_dir: str

    :ivar frequency: Epoch interval for running the callback operation. Defaults to 1 (each epoch).
    :type frequency: int

    :ivar embedding_len: Dimensionality of the embeddings produced by the model.
    :type embedding_len: int

    :ivar num_bins: Number of bins in the histogram representing pairwise cosine distances.
    :type num_bins: int

    :ivar loss_margin: Threshold value marked as a reference line in the visualized histogram,
        indicating a separation margin.
    :type loss_margin: float
    """

    def __init__(self,
                 model_for_embeddings,  # Model or sub-model outputting embeddings
                 validation_dataset,
                 validation_steps=None,
                 log_dir='./logs_embeddings',
                 frequency=1,  # Run every 'frequency' epochs
                 embedding_len=128,
                 num_bins=50,
                 loss_margin=1.0):
        super().__init__()
        self.model_for_embeddings = model_for_embeddings
        self.validation_dataset = validation_dataset
        self.validation_steps = validation_steps
        self.log_dir = log_dir
        self.frequency = frequency
        self.embedding_len = embedding_len
        self.num_bins = num_bins
        self.loss_margin = loss_margin
        os.makedirs(self.log_dir, exist_ok=True)

    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % self.frequency == 0:
            self.plot_embedding_distances(epoch)

    def plot_embedding_distances(self, epoch):
        """ Extract embeddings, compute pairwise distances, and plot histogram """
        embeddings = []

        try:
            val_itr = iter(self.validation_dataset)
            for _ in range(self.validation_steps):
                x, _ = next(val_itr)
                result = self.model_for_embeddings(x, training=False)
                if isinstance(result, list) or isinstance(result, tuple):
                    result = result[0]  # Extract actual embeddings if wrapped in tuple
                embeddings.extend(result.detach().cpu().numpy())
        except StopIteration:
            pass
        
        embeddings = np.array(embeddings)

        # Compute pairwise cosine distances
        pairwise_distances = pdist(embeddings, metric='cosine')  # Condensed pairwise distance matrix

        # Plot histogram
        plt.figure(figsize=(10, 5))
        plt.hist(pairwise_distances, bins=self.num_bins, alpha=0.7, color="blue", edgecolor="black")
        plt.axvline(x=self.loss_margin, color="red", linestyle="dotted", label=f"Margin ({self.loss_margin:.2f})")
        # plt.axvline(x=2.0, color="black", linestyle="dashed", label="Max Distance (2.0)")
        plt.xlabel("Cosine Distance")
        plt.ylabel("Frequency")
        plt.title(f"Histogram of Pairwise Cosine Distances (Epoch {epoch + 1})")
        plt.legend()

        # Save plot
        plot_path = os.path.join(self.log_dir, f"pairwise_distances_epoch_{epoch + 1}.png")
        plt.savefig(plot_path, dpi=600)
        plt.close()
