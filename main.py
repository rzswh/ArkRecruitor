import slack
import os
from core import response_from_image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--image', default=None, required=False)

args = parser.parse_args()

if __name__ == "__main__":
    if args.image is not None:
        from PIL import Image
        print(response_from_image(open(input('Relative image to test:'), 'rb')))
    else:
        import run_flask
        slack.set_callback(response_from_image)
        run_flask.app.run(port=int(os.environ.get("SLACK_BOT_PORT", 3000)))
