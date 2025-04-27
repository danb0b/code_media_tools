# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 13:48:17 2019

@author: danaukes
"""

#derived from https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

import PIL
import numpy
import scipy.fftpack as fft
from PIL.Image import Image
import matplotlib.pyplot as plt
import os
import yaml
import media_tools.files.support as support
#Image.resize()

#d = 64
#d2 =18

#byte_order = 'big'

def bool_array_to_int(aaa):    
    try:
        aaa = aaa.flatten().tolist()
    except AttributeError:
        pass
    return sum(1<<ii for ii,item in enumerate(reversed(aaa)) if item)    

def int_to_bool_array(phash):
    a1 = numpy.array([((phash>>(ii)&1)) for ii in reversed(range(64))],dtype = numpy.bool)
    a2 = a1.reshape((8,8))
    return a2
    
def square_shrink(i,d):
    i2 = i.resize((d,d),resample = PIL.Image.BILINEAR)
    return i2

def dct2(a):
    return fft.dct( fft.dct( a, axis=0, norm='ortho' ), axis=1, norm='ortho' )

def idct2(a):
    return fft.idct( fft.idct( a, axis=0 , norm='ortho'), axis=1 , norm='ortho')


def gen_p_hash_alt(aname,d=32, d2 = 18):
    i=PIL.Image.open(aname)
    i2 = numpy.array(i)
    p_hash=0
#    shape = i2.shape
#    try:
    found = False
    if len(i2.shape)==3:
        if i2.shape[2]==4:
            i3 = 255-i2[:,:,3]
            i4 = PIL.Image.fromarray(i3)
            a = i4.convert('L')
            found = True
    elif len(i2.shape)==2:
        i3 = 255-(numpy.array((i2/32*255)))
        i3 = numpy.array(i3,dtype=numpy.uint8)
        i4=numpy.array([i3,i3,i3])
        i5 = i4.transpose(1,2,0)
        i6 = PIL.Image.fromarray(i5)
        a = i6.convert('L')#    except IndexError:
        found = True
    if found:
        s = square_shrink(a,d)
        adct = dct2(numpy.array(s))
        adct2 = adct[:d2,:d2]
        mean = adct2.flatten()[1:].mean()
        p_hash  = bool_array_to_int(adct2>mean)
#        try:
            
        
        
#        p_hash=0
        
    return p_hash

def gen_p_hash(aname,d=32, d2 = 18):
    try:
        i=PIL.Image.open(aname)
        a = i.convert('L')
        s = square_shrink(a,d)
        adct = dct2(numpy.array(s))
        adct2 = adct[:d2,:d2]
        mean = adct2.flatten()[1:].mean()
        p_hash  = bool_array_to_int(adct2>mean)
        if p_hash==0:
            p_hash = gen_p_hash_alt(aname,d,d2)
        return p_hash
    except PIL.UnidentifiedImageError:
        return None

def gen_p_hash_opt(aname,d=32, d2 = 18):
    try:
        adct2 = dct2(numpy.array(square_shrink(PIL.Image.open(aname).convert('L'),d)))[:d2,:d2]
        mean = adct2.flatten()[1:].mean()
        p_hash  = bool_array_to_int(adct2>mean)
        if p_hash==0:
            p_hash = gen_p_hash_alt(aname,d,d2)
        return p_hash
    except PIL.UnidentifiedImageError:
        return None

def int_to_img(phash):
    a2=int_to_bool_array(phash)
    i = PIL.Image.fromarray(a2)
    return i

def filter_img_filetype(filename):
    return os.path.splitext(filename)[1].lower() in ['.jpg','.jpeg','.png']
    

        
if __name__=='__main__':
#    p1 = 'C:/Users/danaukes/Dropbox (Personal)/Camera Uploads'    
#    support.rebuild_compare_info(p1,hasher = gen_p_hash_opt,file_filter = filter_img_filetype, filename='image_compare_info.yaml')
#    with open('image_compare_info.yaml') as f:
#        image_compare_info = yaml.load(f,Loader=yaml.FullLoader)
#
#    for key,value in image_compare_info['hash_file_dict'].items():
#        if len(value)>1:
#            print(value)
#        
    p1 = 'C:/Users/danaukes/Dropbox (ASU)/idealab/presentations/2020-03-05 Research Talk/reduced/images-reduced/image330.png'
#    r = gen_p_hash(p1)
    i = PIL.Image.open(p1)
    i2 = numpy.array(i)
    i3 = 255-(numpy.array((i2/32*255)))
    i3 = numpy.array(i3,dtype=numpy.uint8)
    i4=numpy.array([i3,i3,i3])
    i5 = i4.transpose(1,2,0)
    i6 = PIL.Image.fromarray(i5)
#    i3 = 255-i2[:,:,3]
#    i3[:,:,3]=255
#    i4 = PIL.Image.fromarray(i3)
    i7 = i6.convert('L')
#    i5.show()