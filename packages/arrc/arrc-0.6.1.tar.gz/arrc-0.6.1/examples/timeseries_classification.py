# Implement this tutorial from keras to validate model training works.
#
# https://keras.io/examples/timeseries/timeseries_classification_from_scratch/
##############################################################################

import os

import torch

os.environ["KERAS_BACKEND"]="torch"

import keras
from arrc.models import ARRCModel
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import TensorDataset, DataLoader

# Load the FordA Dataset
def readucr(filename):
    data = np.loadtxt(filename, delimiter="\t")
    y = data[:, 0]
    x = data[:, 1:]
    return x, y.astype(int)


root_url = "https://raw.githubusercontent.com/hfawaz/cd-diagram/master/FordA/"

x_train, y_train = readucr(root_url + "FordA_TRAIN.tsv")
x_test, y_test = readucr(root_url + "FordA_TEST.tsv")

# Visualize the data
classes = np.unique(np.concatenate((y_train, y_test), axis=0))

plt.figure()
for c in classes:
    c_x_train = x_train[y_train == c]
    plt.plot(c_x_train[0], label="class " + str(c))
plt.legend(loc="best")
plt.show()
plt.close()

# Standardize the data
x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], 1))
x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], 1))

num_classes = len(np.unique(y_train))
idx = np.random.permutation(len(x_train))
x_train = x_train[idx]
y_train = y_train[idx]
y_train[y_train == -1] = 0
y_test[y_test == -1] = 0

# ARRC expects 1-indexed labels
y_test = y_test + 1
y_train = y_train + 1

train_data = DataLoader(
    TensorDataset(
        torch.from_numpy(x_train).float(),
        torch.from_numpy(y_train).long(),
    ),
    batch_size=32,
    shuffle=True,)

test_data = DataLoader(
    TensorDataset(
        torch.from_numpy(x_test).float(),
        torch.from_numpy(y_test).long(),
    ),
    batch_size=32,
    shuffle=True,)

# Build a model
def make_keras_model(input_shape):
    input_layer = keras.layers.Input(input_shape)

    conv1 = keras.layers.Conv1D(filters=64, kernel_size=3, padding="same")(input_layer)
    conv1 = keras.layers.BatchNormalization()(conv1)
    conv1 = keras.layers.ReLU()(conv1)

    conv2 = keras.layers.Conv1D(filters=64, kernel_size=3, padding="same")(conv1)
    conv2 = keras.layers.BatchNormalization()(conv2)
    conv2 = keras.layers.ReLU()(conv2)

    conv3 = keras.layers.Conv1D(filters=64, kernel_size=3, padding="same")(conv2)
    conv3 = keras.layers.BatchNormalization()(conv3)
    conv3 = keras.layers.ReLU()(conv3)

    gap = keras.layers.GlobalAveragePooling1D()(conv3)
    output_layer = keras.layers.Dense(num_classes, activation="softmax")(gap)

    return keras.models.Model(inputs=input_layer, outputs=output_layer)

# Build a model
def make_arrc_model(input_shape):
    input_layer = keras.layers.Input(input_shape)

    conv1 = keras.layers.Conv1D(filters=64, kernel_size=3, padding="same")(input_layer)
    conv1 = keras.layers.BatchNormalization()(conv1)
    conv1 = keras.layers.ReLU()(conv1)

    conv2 = keras.layers.Conv1D(filters=64, kernel_size=3, padding="same")(conv1)
    conv2 = keras.layers.BatchNormalization()(conv2)
    conv2 = keras.layers.ReLU()(conv2)

    conv3 = keras.layers.Conv1D(filters=64, kernel_size=3, padding="same")(conv2)
    conv3 = keras.layers.BatchNormalization()(conv3)
    conv3 = keras.layers.ReLU()(conv3)

    gap = keras.layers.GlobalAveragePooling1D()(conv3)

    return ARRCModel.BuildARRCModel(
        inputs = input_layer,
        embedding_outputs = gap,
        num_classes = num_classes,
    )


epochs = 500
batch_size = 32
callbacks = [
    keras.callbacks.ModelCheckpoint(
        "best_model.keras", save_best_only=True, monitor="val_loss"
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.5, patience=20, min_lr=0.0001
    ),
    keras.callbacks.EarlyStopping(monitor="val_loss", restore_best_weights=True, patience=50, verbose=1),
]

# # Train the model - ARRC VERSION
model = make_arrc_model(input_shape=x_train.shape[1:])
loss_fn_map, loss_wgt_map = ARRCModel.BuildARRCLossMapsForModel(
    model,
    classification_loss_fn=keras.losses.SparseCategoricalCrossentropy(),
    embedding_loss_fn=None,
    logits_loss_fn=None,
)
model.loss_fn_map = loss_fn_map
model.loss_wgt_map = loss_wgt_map
model.add_classification_metric(keras.metrics.SparseCategoricalAccuracy(name="acc"))
keras.utils.plot_model(model, show_shapes=True)

optimizer = keras.optimizers.Adam()
model.summary()
model.arrc_fit(
    optimizer=optimizer,
    dataloader=train_data,
    validation_dataloader=test_data,
    epochs=epochs,
    steps_per_epoch=len(train_data),
    validation_steps=len(test_data),
    callbacks=callbacks,
)


# NOW KERAS VERSION
# model = make_keras_model(input_shape=x_train.shape[1:])
# model.compile(
#     optimizer="adam",
#     loss="sparse_categorical_crossentropy",
#     metrics=["sparse_categorical_accuracy"],
# )
# history = model.fit(
#     x_train,
#     y_train,
#     batch_size=batch_size,
#     epochs=epochs,
#     callbacks=callbacks,
#     validation_split=0.2,
#     verbose=1,
# )
#
# model = keras.models.load_model("best_model.keras")
# test_loss, test_acc = model.evaluate(x_test, y_test)
# print("Test accuracy", test_acc)
# print("Test loss", test_loss)


# NOW KERAS VERSION EXCEPT USING DATALOADER WRAPPERS
# model = make_keras_model(input_shape=x_train.shape[1:])
# model.summary()
# model.compile(
#     optimizer="adam",
#     loss="sparse_categorical_crossentropy",
#     metrics=["sparse_categorical_accuracy"],
# )
# history = model.fit(
#     train_data,
#     validation_data=test_data,
#     batch_size=batch_size,
#     epochs=epochs,
#     callbacks=callbacks,
#     verbose=1,
# )

# NOW KERAS VERSION EXCEPT USING DATALOADER WRAPPERS and WITHOUT NAMED COMPILE OPTIONS
# model = make_keras_model(input_shape=x_train.shape[1:])
# model.summary()
# model.compile(
#     optimizer=keras.optimizers.Adam(),
#     loss=keras.losses.SparseCategoricalCrossentropy(),
#     metrics=["sparse_categorical_accuracy"],
# )
# history = model.fit(
#     train_data,
#     validation_data=test_data,
#     batch_size=batch_size,
#     epochs=epochs,
#     callbacks=callbacks,
#     verbose=1,
# )


# model = keras.models.load_model("best_model.keras")
output = model.evaluate(test_data)
print()
names = model.metrics_names
print(f"Got {len(output)} results with {len(names)} names: {names}")
for name, value in zip(names, output):
    print(f"{name}: {value}")
