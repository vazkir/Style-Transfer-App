Style Transfer App
==============================
Harvard AC215



## Setup

### MacOS Installation

You can create the required MacOs conda env with

```bash
conda env create -f environment.yml
```

Then you can start the conda env with:

```bash
conda activate MLOpsProject
```

### Windows Installation
The environment.yml contains tensorflow packages specific to MacOS like "tensorflow-macos" and "tensorflow-metal". So you would probably need to remove those and maybe any required tensorflow package to get it to install.

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
python -m data_collection.pinterest -t -mc 3 "dotpainting_on_rocks" -u "https://nl.pinterest.com/ideas/architecture/918105274631/"
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