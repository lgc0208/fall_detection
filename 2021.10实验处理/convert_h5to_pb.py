#convert_h5to_pb.py
"""
Created on Sun Nov 28 20:24:40 2021

@author:LIN Guocheng
@email: lgc0208@bupt.edu.cn

Description:
"""

import tensorflow as tf
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2
 
def convert_h5to_pb():
    model = tf.keras.models.load_model("./model/LSTM.h5",compile=False)
    model.summary()
    full_model = tf.function(lambda Input: model(Input))
    full_model = full_model.get_concrete_function(tf.TensorSpec(model.inputs[0].shape, model.inputs[0].dtype))
 
    # Get frozen ConcreteFunction
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
 
    # Save frozen graph from frozen ConcreteFunction to hard drive
    tf.io.write_graph(graph_or_graph_def=frozen_func.graph,
                      logdir="model",
                      name="LSTM.pb",
                      as_text=False)
  
convert_h5to_pb()