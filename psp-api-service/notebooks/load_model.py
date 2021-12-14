import os, time
import json
import numpy as np
import onnx
from onnx_tf.backend import prepare
import tensorflow as tf
from tensorflow.python.keras import backend as K
# import tensorflow_hub as hub
# from api.local import RUN_LOCAL
# from PIL import Image


local_models_path = "/persistent/models"
local_onnx_path = "/persistent/onnx"



def get_onnx_tf_model(model_name):
    tic = time.time()

    # Load the model from it's ONNX format
    model = onnx.load(f"{local_onnx_path}/{model_name}.onnx")
    
    # Convert the onnx model to tensorflow
    tf_rep = prepare(model)

    toc = time.time()
    print(f"Loading and converting '{model_name}' onnx to tf took {round(toc - tic, 2)} seconds.")

    return tf_rep



get_onnx_tf_model('psp_ffhq_encode.onnx')

get_onnx_tf_model('cartoon_psp_mobile_256p.onnx')