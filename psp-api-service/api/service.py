import base64
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
import asyncio
# from api.tracker import TrackerService
import pandas as pd
import numpy as np
import os
from fastapi import File
from tempfile import TemporaryDirectory
from api.model import psp_inf

# from api.tracker import TrackerService
# 
# 
# # Initialize Tracker Service
# tracker_service = TrackerService()

local_psp_path = "/persistent/psp"
local_psp_inputs_path = f"{local_psp_path}/inputs"
local_psp_outputs_path = f"{local_psp_path}/outputs"

test_no_models = False
save_persistent = True

# Setup FastAPI app
app = FastAPI(
    title="API Server",
    description="API Server",
    version="v1"
)

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Call the tracker service when the API service starts running.
@app.on_event("startup")
async def startup():
    # Startup tasks
    if not test_no_models:
        psp_inf.load_psp_models()

    psp_inf.load_latent_direction_vectors()


# Routes
@app.get("/")
async def get_index():
    return {
        "message": "Welcome to the API Service"
    }


def run_latent_match(input_img, file_dir):
    start_files_id = datetime.now().strftime('%d-%m-%Y_%H-%M')
    
    image_path_input = os.path.join(file_dir, f"{start_files_id}_img.png")
    
    with open(image_path_input, "wb") as output:
        output.write(input_img)

    # Since inference takes very long we can bypass this for local builds
    if test_no_models:
        matched_img_path = "/persistent/psp/imgs/30-11-2021_23-14_latent_img.png"
        matched_img = input_img
        matched_latent = np.ndarray(shape=(1, 18, 512))
    
    else:
        # Make prediction
        matched_img, matched_latent = psp_inf.get_latent_match_and_img_repr(image_path_input)
        matched_img_path = os.path.join(file_dir, f"{start_files_id}_matched_img.png")
        mathced_latent_path = os.path.join(file_dir, f"{start_files_id}_matched_latent")

        # Save generate image and latent to disk
        matched_img.save(matched_img_path)
        np.save(mathced_latent_path, matched_latent)

    
    # Read image to encoded bytes for response
    with open(matched_img_path, "rb") as image_file:
        encoded_image_string = base64.b64encode(image_file.read())
        
    return encoded_image_string, matched_latent, start_files_id



def run_latent_manipulate(latent_id, inp_latent_path, change_dir_dict):
    # Load the requested latent
    inp_latent = np.load(inp_latent_path)

    # Make prediction
    changed_img, changed_latent = psp_inf.get_mutated_latent(inp_latent, 
                                                             change_dir_dict)
    
    changed_img_path = os.path.join(local_psp_outputs_path, f"{latent_id}_changed_img.png")
    changed_latent_path = os.path.join(local_psp_outputs_path, f"{latent_id}_changed_latent")

    # Save generate image and latent to disk
    changed_img.save(changed_img_path)
    np.save(changed_latent_path, changed_latent)
    
   
    # Read image to encoded bytes for response
    with open(changed_img_path, "rb") as image_file:
        encoded_image_string = base64.b64encode(image_file.read())
        
    return encoded_image_string, changed_latent


@app.post("/mutate_latent")
async def mutate_latent(
    latent_id: str = "01-12-2021_02-08"
):

    latent_path = os.path.join(local_psp_inputs_path, f"{latent_id}_matched_latent.npy")    
    change_age_dir = {'age_degree': 8, 'eye_distance_degree': 0, 'eye_eyebrow_distance_degree': 0,
                            'eye_ratio_degree': 0,  'eyes_open_degree': 0, 'gender_degree': 1, 
                            'lip_ratio_degree': 0, 'mouth_open_degree': 0, 'nose_mouth_distance_degree': 0, 'nose_ratio_degree': 0, 
                            'nose_tip_degree': 0, 'pitch_degree': 0, 'roll_degree': 0, 'smile_degree': 0, 'yaw_degree': 0}


    encoded_image_string = ""
    changed_latent = []
    
    psp_inf.load_psp_models(True)
    
    # Save the image
    if save_persistent:
        encoded_image_string, changed_latent = run_latent_manipulate(latent_id,
                                                                     latent_path, 
                                                                     change_age_dir)
    else:
        with TemporaryDirectory() as image_dir:
            encoded_image_string, changed_latent = run_latent_manipulate(latent_id,
                                                                     latent_path, 
                                                                     change_age_dir)

    # Yields the image itself along with the matched latent variable
    return {
        "mime" : "image/png",
        "changed_img": encoded_image_string,
        "latent_id":latent_id,
        # "changed_latent": changed_latent.tolist()
    }
    

@app.post("/match_latent")
async def match_latent(
        file: bytes = File(...)
):
    print("image file:", len(file), type(file))

    matched_latent = []
    encoded_image_string = ""
    
    # Save the image
    if save_persistent:
        encoded_image_string, matched_latent, start_files_id = run_latent_match(file, local_psp_inputs_path)
    else:
        with TemporaryDirectory() as image_dir:
            encoded_image_string, matched_latent, start_files_id = run_latent_match(file, image_dir)

    # Yields the image itself along with the matched latent variable
    return {
        "mime" : "image/png",
        "matched_img": encoded_image_string,
        "start_files_id":start_files_id,
        # "matched_latent": matched_latent.tolist()
    }
    



# @app.get("/leaderboard")
# def leaderboard_fetch():
#     # Fetch leaderboard
#     df = pd.read_csv("/persistent/experiments/leaderboard.csv")

#     df["id"] = df.index
#     df = df.fillna('')

#     return df.to_dict('records')


# @app.get("/best_model")
# async def get_best_model():
#     model.check_model_change()
#     if model.best_model is None:
#         return {"message": 'No model available to serve'}
#     else:
#         return {
#             "message": 'Current model being served:'+model.best_model["model_name"],
#             "model_details": model.best_model
#         }
