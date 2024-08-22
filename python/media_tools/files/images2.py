from PIL import Image
import imagehash
import os

def filter_img_filetype(filename):
    return os.path.splitext(filename)[1].lower() in ['.jpg','.jpeg','.png']

def my_p_hash(filename):
    hash = imagehash.phash(Image.open(filename))
    return str(hash)