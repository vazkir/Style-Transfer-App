import base64
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


test_no_models = True

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



@app.post("/match_latent")
async def predict(
        file: bytes = File(...)
):
    print("image file:", len(file), type(file))

    # Save the image
    with TemporaryDirectory() as image_dir:
        image_path_input = os.path.join(image_dir, "input_img.png")
        with open(image_path_input, "wb") as output:
            output.write(file)


        if not test_no_models:
            # Make prediction
            matched_img, matched_latent = psp_inf.get_latent_match_and_img_repr(image_path_input)
        

            # Save generate image to tempdir
            image_path_latent = os.path.join(image_dir, "latent_match_img.png")
            matched_img.save(image_path_latent)
            
        else:
            image_path_latent = image_path_input
            matched_latent = np.ndarray(shape=(1, 18, 512))
        
        # Read image to encoded bytes for response
        with open(image_path_latent, "rb") as image_file:
            encoded_image_string = base64.b64encode(image_file.read())

        payload = {
            "mime" : "image/png",
            "image": encoded_image_string,
            "matched_latent": matched_latent.tolist()
        }
        
        return payload




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
