# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 11:07:21 2021

@author: danaukes
"""
import os
import fitz

path = r'C:\Users\danaukes\Desktop'
path_out = os.path.join(path,'output')
os.makedirs(path_out)

file = os.path.join(path,'biomechanics.pdf')
doc = fitz.open(file)
for i in range(len(doc)):
    for img in doc.getPageImageList(i):
        xref = img[0]
        pix1 = fitz.Pixmap(doc, xref)
        if (pix1.n - pix1.alpha) < 4:       # this is GRAY or RGB
            pix1.writePNG(os.path.join(path_out,"p%s-%s.png" % (i, xref)))
        else:               # CMYK: convert to RGB first
            pix1 = fitz.Pixmap(fitz.csRGB, pix1)
            pix1.writePNG(os.path.join(path_out,"p%s-%s.png" % (i, xref)))
            pix1 = None
        pix = None
