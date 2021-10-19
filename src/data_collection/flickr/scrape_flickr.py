# 2 Main sources
# Library with api: https://github.com/sybrenstuvel/flickrapi
# Somebody who used api to download: https://github.com/ultralytics/flickr_scraper
import time, os, random
from pprint import pprint
from flickrapi import FlickrAPI
import pandas as pd
from data_collection.download_img import download_uri
from dotenv import load_dotenv

from data_collection.download_imgs_pooled import download_imgs_threaded

load_dotenv()
key = os.environ["FLICKR_KEY"]
secret = os.environ["FLICKR_SECRET"]


def etree_to_dict(t):
    d = {t.tag : map(etree_to_dict, t.iterchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
    d['text'] = t.text
    return d


def get_urls(image_tag, max_count, download=True):
    print(f"Starting Flickr downloads from tag '{image_tag}' with max count -> {max_count}..")
    
    t = time.time()

    flickr = FlickrAPI(key, secret)
    photos = flickr.walk(text=image_tag,
                            tag_mode='all', # # 'any' for an OR combination of tags // 'all' for an an AND combination. 
                            tags=image_tag,
                            extras='url_o',
                            per_page=500,
                            sort='relevance')


    # Where to store
    data_dir = f"data/flickr/{image_tag}"
    img_downl_dir = f"{data_dir}/imgs"

    if download:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        if not os.path.exists(img_downl_dir):
            os.makedirs(img_downl_dir)


    # Img data to store in CSV
    all_img_data = []
    all_urls = []
    succes_count = 0

    for i, photo in enumerate(photos):

        # Grab the current image's flicker API data
        img_data = dict(photo.items())
        # pprint(img_data)

        if i < max_count:
            try:
                url=img_data.get('url_o') 
                print(url)
                if url is None:
                    url = 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % \
                          (img_data.get('farm'), img_data.get('server'), img_data.get('id'), img_data.get('secret'))  # large size


                # Add field for url we downloaded from
                img_data['download_url'] = url
                all_urls.append(url)

                # Update img info and succes rate
                all_img_data.append(img_data)
                succes_count += 1
                
            except:
                print('%g/%g error...' % (i, max_count))
        else:
            print("Done grabbing Flirckr urls to download. Succces {} urls out of {}".format(succes_count, max_count))
            break
    
    
    # Download the actual images
    download_results = download_imgs_threaded(all_urls, img_downl_dir)

    # Create df from default flickr img data and add url response column
    df = pd.DataFrame.from_dict(all_img_data, orient='columns')
    df['url_response'] = download_results['response']

    # Save img data to disk as CSV
    df.to_csv(f"{data_dir}/img_data.csv")

    print('Done with  scraping. (%.1fs)' % (time.time() - t) + ('\nAll images saved to %s' % img_downl_dir))

    print(f"Done with Flickr scraping for tag '{image_tag}'. {round((time.time() - t),1)}")
    print(f"All images saved to '{img_downl_dir}")


def main(call_args):

    # Grab and construct vars to pass on
    tag = call_args["tag"]
    max_count = call_args["max_count"]

    # Download data from api
    get_urls(tag, max_count)

