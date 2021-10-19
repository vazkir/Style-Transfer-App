# Main sources
# Got idea from: https://towardsdatascience.com/how-to-use-flickr-api-to-collect-data-for-deep-learning-experiments-209b55a09628
# Github repo: https://github.com/xjdeng/pinterest-image-scraper
# Somebody who used api to download: https://github.com/ultralytics/flickr_scraper
import time, os
import pandas as pd
from dotenv import load_dotenv
from .scraper import Pinterest_Helper
from data_collection.download_imgs_pooled import download_imgs_threaded

# Login credentials
load_dotenv()
user = os.environ["PINTEREST_USER"]
password = os.environ["PINTEREST_PASS"]

# Functionality to scrape the data
def get_images(pintr_url, tag, max_count, scroll_threshold = 500):
    print(f"Starting Pinterest downloads from tag '{pintr_url}'..")
    t = time.time()

    # Where to store
    data_dir = f"data/pinterest/{tag}"
    img_downl_dir = f"{data_dir}/imgs"

    # Also .csv with general info stored in here
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.path.exists(img_downl_dir):
        os.makedirs(img_downl_dir)


    # Initialize
    ph = Pinterest_Helper(user, password, max_count, scroll_threshold)
    images = ph.runme(pintr_url)

    # To store decoded img url strings, see issue:
    # https://github.com/xjdeng/pinterest-image-scraper/issues/7#issuecomment-529890587
    img_urls = []
    
    for i in images:
        img_urls.append(i.decode())

    print("Done scrolling! Now let's start downloading...")

    print(img_urls)
    # Download the actual images
    download_results = download_imgs_threaded(img_urls, img_downl_dir)

    # Write source urls to disk
    img_info_df = pd.DataFrame.from_dict(download_results, orient='columns')
    img_info_df['tag'] = tag

    img_csv_filename = f"{data_dir}/img_data.csv"
    img_info_df.to_csv(img_csv_filename)

    print(f"Done with Pintest scraping for tag '{tag}'. {round((time.time() - t),1)}")
    print(f"All images saved to '{img_downl_dir}")


def main(call_args):

    # Grab and construct vars to pass on
    pintr_url = call_args["url"]
    tag = call_args["tag"]
    max_count = call_args["max_count"]
    scroll_threshold = call_args["scroll_threshold"]

    
    # Download data from api
    get_images(pintr_url, tag, max_count, scroll_threshold)

