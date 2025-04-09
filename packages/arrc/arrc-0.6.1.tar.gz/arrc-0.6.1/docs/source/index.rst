.. Affective Research Dataset Toolkit documentation master file, created by
   sphinx-quickstart on Wed Mar 19 13:07:36 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Affective Research on Representations and Classifications (ARRC)
================================================================

Welcome
-------

Affective Research on Representations and Classifications (ARRC) is an open-source
framework for AER model development. It is written using the multi-backend Keras 3.0
API with support for both Tensorflow and PyTorch backends. The core of
ARRC is the ARRCModel class that encapsulates a user-defined feature extractor. ARRCModel
provides an optional classification head, enabling it to be used for metric learning and classification problems alike. Loss functions can be applied to embedding output or classification
output layers separately or as weighted losses applied to both simultaneously. The ARRC
source code includes implementations of the feature extractors described in Section
7.2, and is compatible with any Keras, Tensorflow or PyTorch loss function.
ARRC also provides several custom layers used for data augmentation during training.
The available data augmentations include additive Gaussian noise, random time shift, and
random amplitude scaling

Start with `the quick start guide <user_guide/index.html>`_, or dive deep in the `API reference guide <reference/index.html>`_.

.. toctree::
    :hidden:
    :titlesonly:

    user_guide/index
    reference/index
    changelog