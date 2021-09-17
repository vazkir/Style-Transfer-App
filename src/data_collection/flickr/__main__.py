from .scrape_flickr import main
import argparse


# Arguments that can be used
# https://stackoverflow.com/a/8493862/8970591
parser = argparse.ArgumentParser(
    description="Arguments to pass to the flickr api for images you want to download"
)

parser.add_argument(
    "-t",
    "--image_tag", # Namespace
    type=str,
    default="cars",
    help="The Flickr tag you want the images from scraped",
)

parser.add_argument(
    "-mc",
    "--max_count", # Namespace
    type=int,
    default=5,
    help="Amount of images you want to download from the flickr API",
)



# Grab or default script argument
args = parser.parse_args()


if __name__ == "__main__":
    # Set args to dict that is also easier testable
    call_args = {"tag": args.image_tag, "max_count": args.max_count}

    # Main as function makes it testable
    main(call_args)

