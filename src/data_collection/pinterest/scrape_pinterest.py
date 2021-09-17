# Main sources
# Got idea from: https://towardsdatascience.com/how-to-use-flickr-api-to-collect-data-for-deep-learning-experiments-209b55a09628
# Github repo: https://github.com/xjdeng/pinterest-image-scraper
# Somebody who used api to download: https://github.com/ultralytics/flickr_scraper
import time, os, random, pprint
from .scraper import Pinterest_Helper, download
import pandas as pd

# Login credentials
user = os.environ["PINTEREST_USER"]
password = os.environ["PINTEREST_PASS"]

# Functionality to scrape the data
def get_images(pintr_url, tag):
    print(f"Starting Pinterest downloads from tag '{pintr_url}'..")
    t = time.time()

    # Where to store
    data_dir = f"data/pinterest/{tag}"
    img_downl_dir = f"{data_dir}/imgs"

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        os.makedirs(img_downl_dir)

    # Initialize
    ph = Pinterest_Helper(user, password)
    images = ph.runme(pintr_url)

    # To store decoded img url strings, see issue:
    # https://github.com/xjdeng/pinterest-image-scraper/issues/7#issuecomment-529890587
    img_urls = []
    
    for i in images:
        img_urls.append(i.decode())


    print("Done scrolling! Now let's start downloading...")

    # Download them
    download(img_urls, img_downl_dir)

    # Write source urls to disk
    img_urls = pd.Series(img_urls)
    img_csv_filename = f"{data_dir}/img_data.csv"
    img_urls.to_csv(img_csv_filename)

    print('Done. (%.1fs)' % (time.time() - t) + ('\nAll images saved to %s' % img_csv_filename))


def main(call_args):

    # Grab and construct vars to pass on
    pintr_url = call_args["url"]
    tag = call_args["tag"]
    
    # Download data from api
    get_images(pintr_url, tag)

