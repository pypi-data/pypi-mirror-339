import keras
import arrc.ops as aops

class PairwiseDistanceMetric(keras.metrics.Metric):
    def __init__(self, name, dtype="float64", **kwargs):
        super().__init__(name=name, dtype=dtype, **kwargs)
        self.total = self.add_weight(name="total", initializer="zeros", dtype=dtype)
        self.count = self.add_weight(name="count", initializer="zeros", dtype=dtype)

    def _pairwise_distances(self, embeddings):
        expanded_a = keras.ops.expand_dims(embeddings, axis=1)  # (batch, 1, dim)
        expanded_b = keras.ops.expand_dims(embeddings, axis=0)  # (1, batch, dim)
        return keras.ops.norm(expanded_a - expanded_b, axis=-1)  # (batch, batch)

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true = keras.ops.reshape(y_true, [-1])  # (batch,)
        y_pred = keras.ops.reshape(y_pred, [keras.ops.shape(y_true)[0], -1])  # (batch, embedding_dim)

        pairwise_dist = self._pairwise_distances(y_pred)
        labels_equal = keras.ops.equal(keras.ops.expand_dims(y_true, 1), keras.ops.expand_dims(y_true, 0))
        mask_off_diag = ~ keras.ops.eye(keras.ops.shape(y_true)[0], dtype="bool")

        mask = self._build_mask(labels_equal, mask_off_diag)
        distances = aops.boolean_mask(pairwise_dist, mask)

        self.total.assign_add(keras.ops.sum(distances))
        self.count.assign_add(keras.ops.sum(keras.ops.cast(mask,"int")))

    def result(self):
        return keras.ops.divide_no_nan(self.total, self.count)

    def reset_state(self):
        self.total.assign(0.0)
        self.count.assign(0.0)

    def _build_mask(self, labels_equal, mask_off_diag):
        raise NotImplementedError("Subclasses must implement _build_mask()")

class IntraClassDistance(PairwiseDistanceMetric):
    def __init__(self, name="intra_class_distance", **kwargs):
        super().__init__(name=name, **kwargs)

    def _build_mask(self, labels_equal, mask_off_diag):
        return keras.ops.logical_and(labels_equal, mask_off_diag)

class InterClassDistance(PairwiseDistanceMetric):
    def __init__(self, name="inter_class_distance", **kwargs):
        super().__init__(name=name, **kwargs)

    def _build_mask(self, labels_equal, mask_off_diag):
        return keras.ops.logical_and(keras.ops.logical_not(labels_equal), mask_off_diag)

class NormalizedSeparationMetric(keras.metrics.Metric):
    def __init__(self, name="norm_sep", **kwargs):
        super().__init__(name=name, **kwargs)
        self.inter = InterClassDistance()
        self.intra = IntraClassDistance()

    def update_state(self, y_true, y_pred, sample_weight=None):
        self.intra.update_state(y_true, y_pred)
        self.inter.update_state(y_true, y_pred)

    def result(self):
        inter = self.inter.result()
        intra = self.intra.result()
        return (inter-intra)/(inter+intra+keras.backend.epsilon())

    def reset_state(self):
        self.intra.reset_state()
        self.inter.reset_state()

class SeparationMetric(keras.metrics.Metric):
    def __init__(self, name="sep", **kwargs):
        super().__init__(name=name, **kwargs)
        self.inter = InterClassDistance()
        self.intra = IntraClassDistance()

    def update_state(self, y_true, y_pred, sample_weight=None):
        self.intra.update_state(y_true, y_pred)
        self.inter.update_state(y_true, y_pred)

    def result(self):
        inter = self.inter.result()
        intra = self.intra.result()
        return (inter-intra)

    def reset_state(self):
        self.intra.reset_state()
        self.inter.reset_state()
