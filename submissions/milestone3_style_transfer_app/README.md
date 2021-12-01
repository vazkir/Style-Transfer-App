Milstone 3 - Style Transfer App
==============================
Harvard AC215


## Notebooks used

Inside the notebooks folder you can find the PSP folder which contains the notebooks we used in colab to:
- Run the original pytorch models
- Convert the pytoch models to ONNX format
- Run the onnx_tf models as tensorflow models

Do note that they have originally been ran in the cloud where have access to other specific PSP folders on where we have pytorch and other tools installed. 

If you want to actually run the notebooks, then please let use know so we can give you access to them.



## PSP API Service

This folder contains the api we created that can do the following:
1) Load onnx_tf models into memory
2) Receive an input image as request which is then converted by our first model called 'psp.onnx' to a latent representation of the image which is returned
3) Receive a latent vector which is then mutated to aplpy an age vector. This mutated vector is then used as input and then run through our second "decoder.onnx" model to generate an image with this mutatation
  - For now we have hardcoded to use the age vector to create an older version of the person in the image


## React Frontend

This contains all our frontend code which leverages the api when an image gets uploaded. Then it gets a latent matched image back from the API. From which the user can then choose to apply an age vector to, to make the current image of a person look older



## Room for improvement


### Model load and inference time
Loading our models into memory already takes more then 2 minutes and gettingt the latent image match from the input image takes more than 10 minutes (!?). As you can notice, this is not optimal for the user experience at all. 

We want to therefore debug our models further in terms of the onnx conversion, since the pytorch model seemed to run way faster. 

### Changing other feature dimensions
Also currently the changing of the image is hardcoded to only change the age vector, while we alreay have the code inplace (which is also tested) to change other dimensions, like eye or gender.

We are planning to implement sliders in the frontend ASAP so the user has more control over how he or she wants to change the image


### Neural Style Transfer
We locally ran notebooks to apply NST, which weren't that fast since the model itself had to train. We have been reading the latest papaers regarding faster style transfer and have found some pre-trained models that can achieve NST within seconds.

We are also planning to get this functionality (besides changing the image in the latent space) to the application as soon as possible.










## Setup

### MacOS Installation

You can create the required MacOs conda env with:

```bash
conda env create -f environment_macos.yml
```

Then you can start the conda env with:

```bash
conda activate MLOpsProject
```

### Windows Installation
The environment.yml contains tensorflow packages specific to MacOS like "tensorflow-macos" and "tensorflow-metal". So you would probably need to remove those and maybe any required tensorflow package to get it to install.
The current (as of 10oct2021) environment.yml file contains the macos packages, but that one can be changed to match the windows installation since there is also a seperate one for macos.


When you updated the existing environment.yml or created your own you can create the conda env with:

```bash
conda env create -f environment.yml
```

Once installed you can start the conda env with:

```bash
conda activate MLOpsProject
```

## Required setup
You will need to create a .env file with following information in the root of the project:
```
export FLICKR_KEY=FILL_OUT
export FLICKR_SECRET=FILL_OUT
export PINTEREST_USER=FILL_OUT
export PINTEREST_PASS=FILL_OUT
```
To obtain this information you will need to [create an account](https://pinterest.com/) on pinterest and [sign up for a Flicker API key](https://identity.flickr.com/sign-up)


## Scraper Usage


### Get to the righ directory!
Move into the src directory before you run the commands listed below:
```bash
cd src
```

### Scrape Flickr -> Pulls data from their api

Flags:
* -t -> Tag to search for on flickr
* -mc -> Max count, meaning max downloaded images

```python
python -m data_collection.flickr -t "dotpainting" -mc 500
```

### Scrape Pinterest -> Scrapes the url with selenium

Flags:
* -t -> Tag name to give the folder of images e.g. the board name like "animals_horses"
* -u -> Url to the actual images you want to scrape
* -mc -> Max count, meaning max downloaded images. 
  - This is not super specific since chrom will scroll and grab all the new images it can find, meaning that the first scroll will already yield about 9 images.


```python
python -m data_collection.pinterest -t "dotpainting_on_rocks" -mc 3 -u "https://nl.pinterest.com/ideas/architecture/918105274631/"
```





Project Organization
------------
      .
      ├── LICENSE
      ├── Makefile
      ├── README.md
      ├── models
      ├── notebooks
      ├── references
      ├── requirements.txt
      ├── setup.py
      ├── src
      │   ├── __init__.py
      │   └── build_features.py
      ├── submissions
      │   ├── milestone1_groupname
      │   ├── milestone2_groupname
      │   ├── milestone3_groupname
      │   └── milestone4_groupname
      └── test_project.py

--------



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)