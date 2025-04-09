# Affective Research on Representations and Classifications
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

Quick Index of this README:
- Want to know if you can use it? Jump to [Intended Use and License](#license)
- Want to know how to use it? Jump to [Quick Start](#quickstart)
- Want to help out? Jump to [Contributing](#contributing)

## Quick Start
__Step 1: Installation__

```bash
pip install arrc
```

## Intended Use and License
<a name="license"></a>
This library is intended for use by only by academic researchers to facilitate advancements in emotion research. It is 
__not for commercial use__ under any circumstances.

This library is licensed under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en) 
International License. 

__You are free to__:
* __Share__ — copy and redistribute the material in any medium or format 
* __Adapt__ — remix, transform, and build upon the material

__Under the followiung terms__:
* __Attribution__ — You must [give appropriate credit](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en#ref-appropriate-credit), provide a link to the license, and [indicate if changes were made](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en#ref-indicate-changes). You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
* __NonCommercial__ — You may not use the material for [commercial purposes](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en#ref-commercial-purposes)
* __ShareALike__ — If you remix, transform, or build upon the material, you must distribute your contributions under the [same license](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en#ref-same-license) as the original.
* __No additional restrictions__ — You may not apply legal terms or [technological measures](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en#ref-technological-measures) that legally restrict others from doing anything the license permits.

## Quick Start 
<a name="quickstart"></a>

```python
import keras
from arrc.models import ARRCModel

ecg_duration_sec = 30 # Seconds
ecg_sample_rate = 256 # Hertz

# Single - channel ECG Input
inputs = keras.Input(shape=(ecg_duration_sec * ecg_sample_rate, 1))
features = keras.layers.Conv1D ( filters =64, kernel_size =7, padding = "same" )(inputs)
features = keras.layers.MaxPooling1D()(features)
features = keras.layers.Conv1D(filters =128, kernel_size =3, padding = "same", activation = 'relu')(features)
features = keras.layers.GlobalMaxPooling1D()(features)

model = ARRCModel.BuildARRCModel(
    inputs = inputs, 
    embedding_outputs = features, 
    num_classes = 4, 
)
model.summary ()
```


## Contributing <a name="contributing"></a>
We are happy to support you by accepting pull requests that make this library more broadly applicable, or by accepting
issues to do the same. If you have an AER dataset you would like us to integrate, please open an issue for that as well, 
but we will be unable to process issues requesting integration with non-AER datasets at this time.

If you would like to get involved by maintaining dataset integrations in other areas of research, please get in touch 
and we'd be happy to have the help!
