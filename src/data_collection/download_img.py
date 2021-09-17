# From: https://github.com/ultralytics/flickr_scraper/blob/66a8f42af171bfd7d5cb3af3172ca7e5469adcc9/utils/general.py#L11
import os
from pathlib import Path

import requests
from PIL import Image


def download_uri(uri, dir='./'):
    # Download a file from a given URI, including minimal checks

    # Download
    f = dir + os.path.basename(uri)  # filename
    with open(f, 'wb') as file:
        file.write(requests.get(uri, timeout=10).content)

    # Rename (remove wildcard characters)
    src = f  # original name
    for c in ['%20', '%', '*', '~', '(', ')']:
        f = f.replace(c, '_')
    f = f[:f.index('?')] if '?' in f else f  # new name
    if src != f:
        os.rename(src, f)  # rename

    # Add suffix (if missing)
    if Path(f).suffix == '':
        src = f  # original name
        f += '.' + Image.open(f).format.lower()  # append PIL format
        os.rename(src, f)  # rename