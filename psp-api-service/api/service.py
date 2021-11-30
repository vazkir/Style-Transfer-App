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

local_psp_output_path = "/persistent/psp"
local_psp_imgs_path = f"{local_psp_output_path}/imgs"

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


# Routes
@app.get("/")
async def get_index():
    return {
        "message": "Welcome to the API Service"
    }


def run_latent_match(input_img, image_dir):
    start_img = datetime.now().strftime('%d-%m-%Y_%H-%M')
    
    image_path_input = os.path.join(image_dir, f"{start_img}_img.png")
    
    with open(image_path_input, "wb") as output:
        output.write(input_img)

    # Since inference takes very long we can bypass this for local builds
    if test_no_models:
        image_path_latent = image_path_input
        matched_img = input_img
        matched_latent = np.ndarray(shape=(1, 18, 512))
    
    else:
        # Make prediction
        matched_img, matched_latent = psp_inf.get_latent_match_and_img_repr(image_path_input)
        image_path_latent = os.path.join(image_dir, f"{start_img}_latent_img.png")
        
        # Save generate image to disk
        matched_img.save(image_path_latent)
    
    # Read image to encoded bytes for response
    with open(image_path_latent, "rb") as image_file:
        encoded_image_string = base64.b64encode(image_file.read())
        
    return encoded_image_string, matched_latent


@app.post("/match_latent")
async def predict(
        file: bytes = File(...)
):
    print("image file:", len(file), type(file))

    encoded_image_string = ""
    matched_latent = []
    
    # Save the image
    if save_persistent:
        encoded_image_string,  matched_latent = run_latent_match(file, local_psp_imgs_path)
    else:
        with TemporaryDirectory() as image_dir:
            encoded_image_string,  matched_latent = run_latent_match(file, image_dir)

    # Yields the image itself along with the matched latent variable
    return {
        "mime" : "image/png",
        "matched_img": encoded_image_string,
        "matched_latent": matched_latent.tolist()
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
