import cnocr
from PIL import Image
from numpy import array as nparray

model = cnocr.CnOcr(model_name='conv-lite-fc')

Scale = 1.0 / 1080
Left = (784 - 2400 // 2) * Scale
Right = (1536 - 2400 // 2) * Scale
Top = 522 * Scale
Bottom = 737 * Scale

# TopLeft: col, row = 784, 528
# BottomRight: col, row = 1536, 731
# Total: 2399, 1079

def crop(img: Image):
    H, W = img.height, img.width
    top = H * Top
    left = W // 2 + Left * H
    block_width = (Right - Left) * H / 3
    block_height = (Bottom - Top) * H / 2
    pieces = []
    Rv, Rh = 0.18, 0.08
    for i in range(5):
        x, y = left + block_width * ((i % 3) + Rh), top + block_height * ((i // 3) + Rv)
        p = img.crop((x, y, x + block_width * (1 - 2 * Rh), y + block_height * (1 - 2 * Rv)))
        p = p.convert('L') # Grey mode
        pieces.append(p)
    return pieces

'''
Convert image to candidate tags.
'''
def ocr_recogn(img: Image):
    ret = []
    pieces = crop(img)
    for img in pieces:
        label = model.ocr_for_single_line(nparray(img))
        if len(label) == 0:
            print('[Error] OCR failed for the tag. Please check tags are splitted correctly.')
        else:
            ret.append(''.join(label))
    return ret
    