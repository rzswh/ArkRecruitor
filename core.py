
from ocr import *
import re
from urllib import request
import json

class Calculator:

    def __init__(self):
        self.updateList()
        print(self.tags)
        print(self.operators)

    def distance(self, a, b):
        # Edit distance
        A, B = len(a), len(b)
        MAX = A + B
        distance = [0] * (MAX + 1)
        for s in range(1, MAX + 1):
            for i in range(max(0, s - B), min(A, s) + 1):
                j = s - i
                if i == 0 or j == 0 or a[i - 1] != b[j - 1]:
                    distance[j - i] += 1
                if i > 0:
                    distance[j - i] = min(distance[j - i], distance[j - (i - 1)] + 1)
                if j > 0:
                    distance[j - i] = min(distance[j - i], distance[(j - 1) - i] + 1)
        return distance[B - A]

    def matchTag(self, tag):
        minerror, mintag = len(tag), ''
        for t in self.tags:
            error = self.distance(t, tag)
            if error < minerror:
                minerror, mintag = error, t
        return mintag

    def img2tags(self, img):
        tags = ocr_recogn(img)
        print('Recognized tags: %r' % tags)
        tags = [self.matchTag(t) for t in tags]
        print('Corrected tags: %r' % tags)
        return tags

    def listSrcURL(self):
        url_index = 'https://www.bigfun.cn/tools/aktools/hr'
        try:
            result = request.urlopen(url_index).read()
            dataversion = re.search('window.data_version=(\d+)', result.decode()).groups()[0]
            return 'https://www.bigfun.cn/static/aktools/%s/data/akhr.json' % dataversion
        except Exception as e:
            print('Error while loading Bigfun recruitment index.')
            return ''

    def updateList(self):
        self.operators, self.tags = self.getList()

    def getList(self):
        url = self.listSrcURL()
        try:
            result = request.urlopen(url).read()
            result = json.loads(result)
        except Exception as e:
            print('Error while loading recruitment list.')
            print(e)
            return [], set()
        return [{
            'name': x['name'],
            'type': x['type'] + "干员",
            'star': x['level'],
            'tags': x['tags'] + [x['type'] + "干员"]
        } for x in result], set.union(
            *[set(x['tags']) for x in result],
            *[set([x['type'] + "干员"]) for x in result]
        )

    def search_combination(self, tags):
        trivial = []
        solution = []
        for o in self.operators:
            opr_tags = [o['type']] + o['tags']
            if set(opr_tags).issuperset(set(tags)):
                if o['star'] in [2, 3]:
                    trivial.append(o)
                elif o['star'] != 6 or '高级资深干员' in tags:
                    solution.append(o)
        # print(trivial, solution)
        return trivial, solution

    def tags2opers(self, tags):
        found = []
        fail = [False] * 2 ** 5
        for i in range(1, 1 << 5):
            if fail[i]: continue
            subtags = [tags[j] for j in range(5) if (i & (1 << j)) != 0]
            if len(subtags) > 3: continue
            trivial, solution = self.search_combination(subtags)
            if len(trivial) > 0:
                continue
            if len(solution) > 0:
                found.append((solution, subtags))
                # print('%r %r' % (solution, subtags))
            else:
                ii = i
                while ii < 2**5:
                    fail[ii] = True
                    ii = (ii + 1) | i
        return found

    def img2opers(self, img):
        img_tags = self.img2tags(img)
        found = self.tags2opers(img_tags)
        return img_tags, found

calc = None

def get_calc():
    global calc
    if calc is None:
        calc = Calculator()
    return calc

def response_from_image(img):
    from PIL import Image
    from io import BytesIO, IOBase

    if isinstance(img, bytes):
        img = Image.open(BytesIO(img))
    elif isinstance(img, IOBase):
        img = Image.open(img)
    else:
        try:
            assert isinstance(img, Image.Image)
        except AssertionError as e:
            print('Image type not supported. type=%r' % type(img))
    
    tags, found = get_calc().img2opers(img)
    return generate_summary(tags, found)

def response_from_tags(tags):
    calc = get_calc()
    tags = [calc.matchTag(t) for t in tags]
    found = calc.tags2opers(tags)
    return generate_summary(tags, found)

def generate_summary(tags, found):
    summary = 'Tags: %s' % (','.join(tags))
    if len(found) > 0:
        guarantee = [min([o['star'] for o in sol if o['star'] > 1]) \
            if max([o['star'] for o in sol]) > 1 \
            else 1 \
            for sol, subtags in found]
        summary = '''保底%d星！
%s
%s''' % (
    max(guarantee),
    '\n'.join([
        '%d★保底 组合：%s 干员：%s' % (
            guarantee[i],
            ','.join(found[i][1]),
            ','.join([o['name'] for o in found[i][0]])
        ) for i in range(len(found))
    ]),
    summary
)
    else:
        summary = '无黄票。%s' % summary
    return summary

def refresh_tags():
    get_calc().updateList()