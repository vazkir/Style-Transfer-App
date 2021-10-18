import requests, shutil, random
import concurrent.futures
from time import time as timer
from time import sleep
from multiprocessing import cpu_count
from tqdm import tqdm
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError


def fetch_url(url, save_dir, max_requesttime=5):

    # User agent to mimic request from computer
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    }
    
    # Make the request and save the file to disk
    # future.result() will handle any expections/errors    
    # Make the actual request, set the timeout for no data to 10 seconds
    # and enable streaming responses so we don't have to keep the large files in memory
    response = requests.get(url, headers=headers,
                             timeout=max_requesttime, stream=True)

    # Check if the image was retrieved successfully
    if response.status_code == 200:
        
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        response.raw.decode_content = True

        # Only after confirmation success, and now
        # Grab everything after the last slash
        fileName = f"{save_dir}/{url.split('/')[-1]}"

        # Write to disk with copyfileobje, can be 10x faster, see:
        # https://stackoverflow.com/a/39217788/8970591
        with open(fileName, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

    return response.status_code


def download_imgs_threaded(urls, save_dir, max_batch_pause=2):
    
    # Multi-thread
    t = timer()
    max_threads = cpu_count() 

    results = {
        "urls":[],
        "response":[]
    }

    # Initialize progresss bar
    with tqdm(total=len(urls)) as pbar:


        # We can use a with statement to ensure threads are cleaned up promptly
        # This manages all the threads and the re-usability once 1 task has finisged
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:

            # Start the load operations and mark each future with its URL
            # Future operations to load urls
            future_to_url = {executor.submit(fetch_url, url, save_dir, 5): url for url in urls}
                    
            # Loop through future operations to complete
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]

                try:
                    results["response"].append(future.result())

                except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError) as exc:
                    print(f"Error:\"{exc}\" for {url}")
                    results["response"].append(exc)

                # else:
                #     print(f"page is {url} {result}")
                
                # Save for total download results
                results['urls'].append(url)

                # Update progressbar
                pbar.update(1)
                
                # Take a timeout after each batch of download not to overload server
                # Make it random so it looks less like a bot
                sleep(random.uniform(0, max_batch_pause))


    print(f"Done multi-thread ({max_threads}) downloads -> ({round((timer() - t), 2)})\n")
    return results
