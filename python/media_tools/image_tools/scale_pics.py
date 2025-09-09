# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 14:46:31 2017

@author: daukes
"""

from PIL import Image
import os
import glob
import sys


def crop_center(img,w,h):
    x = img.width/2
    y = img.height/2
    img = img.crop((x-w/2,y-h/2,x+w/2,y+h/2))
    return img

#print('hi')

def crop(img,goal_ratio):
    goal_ratio_r = round(goal_ratio,3)

    actual_ratio = img.width/img.height
    actual_ratio_r = round(actual_ratio,3)

    if actual_ratio_r > goal_ratio_r:
        print('reduce width')
        h = img.height
        w = img.height*goal_ratio
        img = crop_center(img,w,h)

    elif actual_ratio_r < goal_ratio_r:
        print('reduce height')
        w = img.width
        h = img.width/goal_ratio
        img = crop_center(img,w,h)

    return img

def pad_center(img, w,h,color=(255,255,255,0)):
    new_img = Image.new(img.mode, (int(w), int(h)), color)
    
    new_img.paste(img, (int((w-img.width)/2),int((h-img.height)/2)))
    return new_img

def scale_pad(img,dimension,goal_ratio):
    w = img.width
    h = img.height

    if scale_rule == scale_by_max:
        goal = dimension
        scale1 = goal/w
        scale2 = goal/goal_ratio/h
        scale3 = goal/h
        scale4 = goal*goal_ratio/w
        
        scale = min(scale1,scale2,scale3,scale4)
        w_new = w*scale
        h_new = h*scale

    else:
        if scale_rule == scale_by_height:
            h_goal = dimension
            scalew = h_goal*goal_ratio/w
            scaleh = h_goal/h
        if scale_rule == scale_by_width:
            w_goal = dimension
            scalew = w_goal/w
            scaleh = w_goal/goal_ratio/h

        if scalew<scaleh:
            scale = scalew
        else:
            scale = scaleh
    
        w_new = w*scale
        h_new = h*scale
    
        
    if scale_rule == scale_by_max:
        if scale==scale1:
            canvas_w = dimension
            canvas_h = int(dimension/goal_ratio)
        if scale==scale2:
            canvas_w = dimension
            canvas_h = int(dimension/goal_ratio)
        if scale==scale3:
            canvas_w = int(dimension*goal_ratio)
            canvas_h = dimension
        if scale==scale4:
            canvas_w = int(dimension*goal_ratio)
            canvas_h = dimension
            
    if scale_rule == scale_by_height:
        canvas_h = dimension
        canvas_w = int(canvas_h*goal_ratio)
    if scale_rule == scale_by_width:
        canvas_w = dimension
        canvas_h = int(canvas_w/goal_ratio)

    w_new = int(w_new)
    h_new = int(h_new)
    img_new = img.resize((w_new, h_new))
    img_new2 = pad_center(img_new,canvas_w,canvas_h)

    return img_new2
    
def scale_by_width(img,width):
    wpercent = (width / float(img.size[0]))
    if (wpercent<1) or upscale:
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((int(width), hsize))
    return img

def scale_by_height(img,height):
    hpercent = (height / float(img.size[1]))
    if (hpercent<1) or upscale:
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, int(height)))
    return img

def scale_by_max(img,width):
    max_dim = max(img.size)
    wpercent = (width / max_dim)
    if (wpercent<1) or upscale:
        wsize = int((float(img.size[0]) * float(wpercent)))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((wsize, hsize))
    return img
        
def format_float(string1):
    value = string1
    value = value.replace(':','/')
    value = float(eval(value))
    return value
    
if __name__=='__main__':

    extensions = ['jpg','png','gif', 'jpeg']
    #subfolder = 'render'
    curdir = os.path.abspath(os.curdir)
    upper,subfolder = os.path.split(curdir)
    
    print(sys.argv)
    print(curdir)
    
    crop_test =False 
    if '-c' in sys.argv[1:]:
        crop_test =True
    print('crop:', crop_test )

    pad_test =False 
    if '-p' in sys.argv[1:]:
        pad_test=True
    print('pad:', pad_test )

    
    
    goal_ratio = 7/5
    for item in sys.argv[1:]:
        if item.startswith('-a='):
            goal_ratio = format_float(item[3:])
    print('aspectratio',goal_ratio)

    dimension = 400
    for item in sys.argv[1:]:
        if item.startswith('-d='):
            dimension = format_float(item[3:])
        elif item.startswith('-d '):
            dimension = format_float(item[3:])            
    print('dimension',dimension)

    quality = 80
    for item in sys.argv[1:]:
        if item.startswith('-q='):
            quality = format_float(item[3:])
    print('quality',quality)

            
    upscale = False
    if '-u' in sys.argv[1:]:
        upscale = True

    scale_rule = scale_by_max
    if '-w' in sys.argv[1:]:
        scale_rule = scale_by_width
    if '-h' in sys.argv[1:]:
        scale_rule = scale_by_height
    if '-m' in sys.argv[1:]:
        scale_rule = scale_by_max

    if scale_rule==scale_by_max:
        print('scale by max dim')
    elif scale_rule == scale_by_height:
        print('scale by height')
    elif scale_rule == scale_by_width:
        print('scale by width')

    print('upscale: ',upscale)
        
#    if '-a='
#    if '-c=' in sys.argv[1:]:
#        print('crop on')
#    
#    
    if not os.path.exists(subfolder):
        os.mkdir(subfolder)

    folder = os.path.abspath(os.curdir)
    
#    print(arg1,arg2)
    
    path1 = os.path.normpath(os.path.abspath(os.path.curdir))
    
    all_files = os.listdir(path1)
    files = []

    for item in all_files:
        if os.path.splitext(item)[1][1:].lower() in extensions:
            files.append(item)            

    print(files)
        
#    basewidth = 400

#    arg2 = sys.argv[2]
    
    
    for filename in files:
        print(filename)
        img = Image.open(filename)
        b = os.path.split(filename)
    
        if not pad_test:
            if crop_test:    
                img = crop(img,goal_ratio)
                
            img = scale_rule(img,dimension)

        else:    
            img = scale_pad(img,dimension,goal_ratio)

        newfilename = os.path.join(path1,subfolder,b[1])
        #print(newfilename)
        img.save(newfilename,quality=quality)  