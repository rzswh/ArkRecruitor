from core import response_from_tags, get_calc
from core import response_from_image
from main import generate_summary
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--image', default=None, required=False)

args = parser.parse_args()

def testInferring():
    try:
        tags = input().split(',')
    except EOFError as e:
        exit(0)
    calc = get_calc()
    tags = [calc.matchTag(t) for t in tags]
    print('Corrected tags: %r' % tags)
    print(response_from_tags(tags))


if __name__ == "__main__":
    from PIL import Image
    print(response_from_image(open(args.image, 'rb')))
    # while True:
    #     testInferring()
        
