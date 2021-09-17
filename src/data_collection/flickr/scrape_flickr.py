# 2 Main sources
# Library with api: https://github.com/sybrenstuvel/flickrapi
# Somebody who used api to download: https://github.com/ultralytics/flickr_scraper
import time, os, random
from pprint import pprint
from flickrapi import FlickrAPI
import pandas as pd

from data_collection.download_img import download_uri


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
                            tag_mode='all',
                            tags=image_tag,
                            extras='url_o',
                            per_page=500,
                            sort='relevance')

    # Where to store
    data_dir = f"data/flickr/{image_tag}"

    if download:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)


    # Img data to store in CSV
    all_img_data = []
    succes_count = 0

    for i, photo in enumerate(photos):

        # Grab the current image's flicker API data
        img_data = dict(photo.items())

        if i < max_count:
            try:
                url=photo.get('url_o')
                if url is None:
                    url = 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % \
                          (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))  # large size

                # download
                if download:
                    download_uri(url, f"{data_dir}/imgs/")
                    
                    # Small interval to not overload the downloads (between 0 and 1 second)
                    # print(random.uniform(0, 1))
                    time.sleep(random.uniform(0, 1))

                # Add field for url we downloaded from
                img_data['download_url'] = url

                # Update img info and succes rate
                all_img_data.append(img_data)
                succes_count += 1
                print('%g/%g %s' % (i+1, max_count, url))
                


            except:
                print('%g/%g error...' % (i, max_count))
        else:
            print("Done fetching urls, fetched {} urls out of {}".format(succes_count, max_count))
            break
    
    # Save img data to disk as CSV
    print("Writting img information to CSV")
    all_img_data_df = pd.DataFrame.from_dict(all_img_data, orient='columns')
    all_img_data_df.to_csv(f"{data_dir}/img_data.csv")
    # print(all_img_data_df)

    print('Done with all. (%.1fs)' % (time.time() - t) + ('\nAll images saved to %s' % dir if download else ''))



def main(call_args):

    # Grab and construct vars to pass on
    tag = call_args["tag"]
    max_count = call_args["max_count"]

    # Download data from api
    get_urls(tag, max_count)

