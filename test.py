from core import response_from_tags, get_calc
from main import generate_summary

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
    while True:
        testInferring()
        
