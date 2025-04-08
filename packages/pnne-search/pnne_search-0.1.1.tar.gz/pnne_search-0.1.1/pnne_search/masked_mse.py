import tensorflow as tf

@tf.keras.utils.register_keras_serializable()
def masked_mse(y_true, y_pred):
    mask = ~tf.math.is_nan(y_true)
    error = tf.square(tf.where(mask, y_true - y_pred, 0.0))
    loss = tf.reduce_sum(error) / tf.reduce_sum(tf.cast(mask, tf.float32))
    return loss
