"""
    File Name:          h5_to_pb.py
    Author:             LIN Guocheng
    Version:            1.0.0
    Description:        将 h5 模型转换为 pb 模型
"""

import tensorflow as tf
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2


def convert_h5to_pb():
    model = tf.keras.models.load_model("./model/LSTM.h5", compile=False)
    model.summary()
    full_model = tf.function(lambda Input: model(Input))
    full_model = full_model.get_concrete_function(
        tf.TensorSpec(model.inputs[0].shape, model.inputs[0].dtype))

    frozen_func = convert_variables_to_constants_v2(full_model)
    frozen_func.graph.as_graph_def()

    layers = [op.name for op in frozen_func.graph.get_operations()]
    print("-" * 50)
    print("Frozen model layers: ")
    for layer in layers:
        print(layer)

    print("-" * 50)
    print("Frozen model inputs: ")
    print(frozen_func.inputs)
    print("Frozen model outputs: ")
    print(frozen_func.outputs)

    tf.io.write_graph(graph_or_graph_def=frozen_func.graph,
                      logdir="model",
                      name="LSTM.pb",
                      as_text=False)


convert_h5to_pb()
