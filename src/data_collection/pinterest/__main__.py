from .scrape_pinterest import main
import argparse

# dotart canvas:
# "https://nl.pinterest.com/search/pins/?q=dot%20painting%20on%20canvas&rs=guide&term_meta[]=dot%7Ctyped&term_meta[]=painting%7Ctyped&add_refine=dot%20painting%20on%20canvas%7Cguide%7Cword%7C7"


# Arguments that can be used
# https://stackoverflow.com/a/8493862/8970591
parser = argparse.ArgumentParser(
    description="Arguments to pass to the Pinterest api for images you want to download"
)

parser.add_argument(
    "-t",
    "--image_tag", # Namespace
    type=str,
    default="architecture",
    help="The Pinterest tag/name you want the images from scraped",
)

parser.add_argument(
    "-u",
    "--url", # Namespace
    type=str,
    default="https://nl.pinterest.com/ideas/architecture/918105274631",
    help="The Pinterest Board or query url we want to scrape",
)


# Grab or default script argument
args = parser.parse_args()


if __name__ == "__main__":
    # Set args to dict that is also easier testable
    call_args = {"url": args.url, "tag": args.image_tag}

    # Main as function makes it testable
    main(call_args)

