import os, time
import json
import numpy as np
import onnx
from onnx_tf.backend import prepare
import tensorflow as tf
from tensorflow.python.keras import backend as K
# import tensorflow_hub as hub
from api.local import RUN_LOCAL
from PIL import Image


AUTOTUNE = tf.data.experimental.AUTOTUNE
local_experiments_path = "/persistent/experiments"
local_models_path = "/persistent/models"
best_model = None
best_model_id = None
prediction_model = None
data_details = None
image_width = 224
image_height = 224
num_channels = 3
psp_model = None
decoder_model = None


if RUN_LOCAL:
    # Pyenv root is inside this folder
    path_persis_exper =  "../../persistent-folder/experiments"
    local_experiments_path = os.path.join(os.path.dirname(__file__),path_persis_exper)


def get_onnx_tf_model(model_name):
    tic = time.time()

    # Load the model from it's ONNX format
    model = onnx.load(f"{local_models_path}/{model_name}.onnx")
    
    # Convert the onnx model to tensorflow
    tf_rep = prepare(model)

    toc = time.time()
    print(f"Loading and converting '{model_name}' onnx to tf took {round(toc - tic, 2)} seconds.")

    return tf_rep


class PSPInference:
    def __init__(self):
        self.timestamp = 0
        self.psp_model = None
        self.decoder_model = None
        self.current_img_vec = None
        self.current_latent_vec = None

    # Make it async so rest of the startup isn't blocked
    # async def load_psp_models(self):
    def load_psp_models(self):
        print("Start our api service, now loading models into memory.....")
        
        if self.psp_model is None: 
            self.psp_model = get_onnx_tf_model('mnist')
        else:
            print("Psp model was already loaded")
            
        if self.decoder_model is None:
            self.decoder_model = get_onnx_tf_model('decoder')
        else:
            print("Decoder model was already loaded")  
        
        print("Done loading models into memory, ready for action :) :)")
                

    # https://stackoverflow.com/questions/67480507/tensorflow-equivalent-of-pytorchs-transforms-normalize
    def normalize_image_pytorch_style(self, image, mean, std):
        for channel in range(3):
            image[:,:,channel] = (image[:,:,channel] - mean[channel]) / std[channel]
        return image


    # I adjusted the default implementation of tensor2im to not use "to.device()", since it's in tf now
    def tensor2img(self, image_tensor, imtype=np.uint8, normalize=True):
        if normalize:
            image_numpy = (np.transpose(image_tensor, (1, 2, 0)) + 1) / 2.0 * 255.0
        else:
            image_numpy = np.transpose(image_tensor, (1, 2, 0)) * 255.0     
        image_numpy = np.clip(image_numpy, 0, 255)
        if image_numpy.shape[2] == 1 or image_numpy.shape[2] > 3:       
            image_numpy = image_numpy[:,:,0]
        return image_numpy.astype(imtype)


    def load_preprocess_image_from_path(self, img_path):
        print("Image", img_path)
        
        # Open the image into the right dimensions
        img = Image.open(img_path)
        img = img.convert("RGB")
        img = img.resize((256, 256))

        # Normalized img dimensions to between -1 and 1
        # similar to how the original model did this in pytorch
        img_resized = self.normalize_image_pytorch_style(
                            np.array(img) / 255.0, 
                            mean=[0.5, 0.5, 0.5], 
                            std=[0.5, 0.5, 0.5])

        
        # Move color axis to start like model is used to
        img_resized = np.moveaxis(img_resized, 2, 0)

        # Add in the first batch dim
        input_batch_img = np.expand_dims(img_resized, axis=0)

        # Return tf representation with right variable type
        return tf.convert_to_tensor(input_batch_img, dtype='float32')


    def match_latent_space_img(self, img_path):

        print("Starting matching image to latent representation...")
        # Image to run before conversion
        img_tf = self.load_preprocess_image_from_path(img_path)
        
        
        tic = time.time()
        result_img_vec, result_latent_vec = self.psp_model.run(img_tf,
                                                          randomize_noise=False, 
                                                          return_latents= True)
        toc = time.time()
        print('Matching image to latent representation took {:.4f} seconds.'.format(toc - tic))
        
        self.current_latent_vec = result_latent_vec
        self.current_img_vec = result_img_vec
        
        
    def get_latent_match_and_img_repr(self, img_path):
        
        # Runs the psp model to get the latent representation of an image close to input
        self.match_latent_space_img(img_path)
        
        # Reverts all preprocessing on resulting image to get to normal format
        img_arr = self.tensor2img(self.current_img_vec[0])
        
        # Formats image vec to actual image
        return Image.fromarray(img_arr), self.current_latent_vec 
        
        
psp_inf = PSPInference()       
# 
#     def make_prediction(self, image_path):
# 
#         # Load & preprocess
#         test_data = self.load_preprocess_image_from_path(image_path)
# 
# 
#         
# 
# 
#         # Make prediction
#         prediction = prediction_model.predict(test_data)
#         idx = prediction.argmax(axis=1)[0]
#         prediction_label = data_details["index2label"][str(idx)]
# 
#         if prediction_model.layers[-1].activation.__name__ != 'softmax':
#             prediction = tf.nn.softmax(prediction).numpy()
#             print(prediction)
# 
#         poisonous = False
#         if prediction_label == "amanita":
#             poisonous = True
# 
#         return {
#             "input_image_shape": str(test_data.element_spec.shape),
#             "prediction_shape": prediction.shape,
#             "prediction_label": prediction_label,
#             "prediction": prediction.tolist(),
#             "accuracy": round(np.max(prediction)*100, 2),
#             "poisonous": poisonous
#         }
# 




# 
# def load_prediction_model():
#     print("Loading Model...")
#     global prediction_model, data_details
# 
#     best_model_path = os.path.join(
#         local_experiments_path, best_model["user"], best_model["experiment"], best_model["model_name"]+".hdf5")
# 
#     print("best_model_path:", best_model_path)
#     prediction_model = tf.keras.models.load_model(
#         best_model_path, custom_objects={'KerasLayer': hub.KerasLayer})
#     print(prediction_model.summary())
# 
#     data_details_path = os.path.join(
#         local_experiments_path, best_model["user"], best_model["experiment"], "data_details.json")
# 
#     # Load data details
#     with open(data_details_path, 'r') as json_file:
#         data_details = json.load(json_file)
# 

# def check_model_change():
#     global best_model, best_model_id
#     best_model_json = os.path.join(local_experiments_path, "best_model.json")
#     if os.path.exists(best_model_json):
#         with open(best_model_json) as json_file:
#             best_model = json.load(json_file)
# 
#         if best_model_id != best_model["experiment"]:
#             load_prediction_model()
#             best_model_id = best_model["experiment"]

