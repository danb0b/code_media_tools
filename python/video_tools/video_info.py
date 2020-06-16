# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 19:08:40 2019

@author: danaukes
"""

import subprocess
import re
import os
import sys

def parse2(string):
    strings = string.split('\r\n')
    keyval = []
    for item in strings:
        a = item.split('=')
        if len(a)==2:
            keyval.append(tuple(a))
    dict1 = dict(keyval)
    return dict1


def parse(string):
    cont = True

    dicts = []
    while cont:
        a = re.search('\[[A-Z]*\]',string)
        b = re.search('\[/[A-Z]*\]',string)
        if a is not None:
            ii = a.span()[1]
            jj = b.span()[0]
            kk = b.span()[1]
#            print(string[ii:jj])
            dict1 = parse2(string[ii:jj])
            dicts.append(dict1)
            string = string[kk:]
        else:
            cont = False
            
    return dicts

class KeyInfo(object):
    def __init__(self,value):
        self.string = value

        try:
            self.float = self.string_to_float(value)
        except Exception:
            pass

        try:
            self.int = self.string_to_int(value)
        except Exception:
            pass

    @staticmethod    
    def string_to_float(item):
        return float(eval(item))
    @staticmethod
    def string_to_int(item):
        return int(str(eval(item)))
    
        
class StreamInfo(object):
#    convert_to_float = ('duration')
#    convert_to_int = ('index',)
    @classmethod
    def build_from_dict(cls,in1):
        self = cls()
        for key,value in in1.items():
            setattr(self,key,KeyInfo(value))
        return self


class VideoInfo(object):
    def __init__(self,file):
        
        s2 = 'ffprobe -v error -show_format -show_streams '+'"'+file+'"'
        result=subprocess.run(s2, shell=True, capture_output=True)
        self.ffprobe_output = result.stdout.decode()
        self.stream_dicts = parse(self.ffprobe_output)
        self.streams = [StreamInfo.build_from_dict(item) for item in self.stream_dicts]
    

    def get_videos(self):
        f = []
        for stream in self.streams:
            try:
                if stream.codec_type.string == 'video':
                    f.append(stream)
            except AttributeError:
                pass
        return f
    

              
def frame_to_time(frame,frame_rate):
    secs = frame/frame_rate
#    h = int(secs/3600)
#    m = int(secs/60 - h*60)
#    s = int(secs-h*3600-m*60)
#    ms = 
    return '{0:.5f}'.format(secs)


if __name__== '__main__':
    path= 'C:/Users/danaukes/Desktop/Conference Video.mp4'
    
    #s2 = 'ffprobe -v error -show_format -show_streams '+'"'+path+'"'
    #b=subprocess.run(s2, shell=True, capture_output=True)
    #d = b.stdout.decode()
    #e = parse(d)
    ##                c=d.split('/r/n')
    #
    #f = get_videos(e)
    a = VideoInfo(path)
    #g = StreamInfo.build_from_dict(f[0])
    #duration = string_to_num(f[0]['r_frame_rate'])
    f = a.get_videos()
    g = f[0]
    print(g.duration.float)
