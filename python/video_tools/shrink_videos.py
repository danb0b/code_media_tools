# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 16:35:18 2019

@author: danaukes
"""

import argparse
import glob
import os
import yaml
import subprocess
import video_tools.video_info as vi

class Movie(object):
    
    _default_crf = 35
    _default_preset = 'ultrafast'
    _default_video_path = 'videos'
    _default_thumb_path = None
    _default_start_time = None
    _default_end_time = None
    _default_thumb_time = None
    
    @classmethod
    def build_from_dict(cls,dict_in,video_path=None,thumb_path=None,crf=None,preset=None,start_time=None,end_time=None,thumb_time=None):
        video_source = dict_in['video_source']
        try:
            video_dest = dict_in['video_dest']
        except KeyError:
            video_dest = cls.build_video_dest(video_source,video_path or cls._default_video_path)
        try:
            thumb_dest = dict_in['thumb_dest']
        except KeyError:
            thumb_dest = cls.build_thumb_dest(video_source,thumb_path or cls._default_thumb_path)
        try:
            crf= dict_in['crf']
        except KeyError:
            crf= crf or cls._default_crf
        try:
            preset= dict_in['preset']
        except KeyError:
            preset= preset or cls._default_preset
        try:
            start_time = dict_in['start_time']
        except KeyError:
            start_time = start_time or cls._default_start_time 
        try:
            end_time = dict_in['end_time']
        except KeyError:
            end_time = end_time or cls._default_end_time 
        try:
            thumb_time = dict_in['thumb_time']
        except KeyError:
            thumb_time = thumb_time or cls._default_thumb_time
            
        return cls(video_source,video_dest=video_dest,thumb_dest=thumb_dest,crf=crf,preset=preset,start_time=start_time,end_time=end_time,thumb_time=thumb_time)
            
    def __init__(self,video_source,video_dest=None,thumb_dest=None,video_path=None,thumb_path=None,crf=None,preset=None,start_time=None,end_time=None,thumb_time=None):
        self.video_source = video_source
        self.video_dest = video_dest or self.build_video_dest(video_source,video_path or self._default_video_path)
        self.thumb_dest = thumb_dest or self.build_thumb_dest(video_source,thumb_path or self._default_thumb_path)
        self.crf = crf or Movie._default_crf
        self.preset = preset or Movie._default_preset
        self.start_time = start_time
        self.end_time = end_time
        self.thumb_time = thumb_time

    @staticmethod
    def build_video_dest(video_source,video_path):
        if video_path is None:
            return None
        else:
            video_name = os.path.splitext(os.path.split(video_source)[1])[0]
            result = os.path.join(video_path,video_name+'.mp4')
            return result

    @staticmethod    
    def build_thumb_dest(video_source,thumb_path):
        if thumb_path is None:
            return None
        else:
            video_name = os.path.splitext(os.path.split(video_source)[1])[0]
            result = os.path.join(thumb_path,video_name+'.png')
            return result
    
    def compute_thumb_time(self):
        s = self.start_time or 0
        if self.end_time is None:
            info = vi.VideoInfo(self.video_source)
            e = info.get_max_length()
        else:
            e = self.end_time
        m = s+(e-s)/2
        return m
        

    def compose_video_string(self):
        if self.start_time is not None:
            st_string = '-ss {0:.3f} '.format(self.start_time)
        else:
            st_string = ''

        if self.end_time is not None:
            et_string = '-to {0:.3f} '.format(self.end_time)
        else:
            et_string = ''
            
        crf_string = '-crf {0:0.0f} '.format(self.crf)
        preset_string = '-preset {0} '.format(self.preset)
               
        s = 'ffmpeg -i "'+self.video_source+'" ' +st_string+et_string+ '-c:v libx264 -async 1 '+preset_string+crf_string+'"'+self.video_dest+'"'                    
        return s

    def compose_thumb_string(self):
        mt_string = '-ss {0:.3f} '.format(self.thumb_time or self.compute_thumb_time())
        
        s = 'ffmpeg '+mt_string+' -i "'+self.video_source+'" -frames:v 1 "'+self.thumb_dest+'"'
        return s
    
    def process(self,force=False):
        if self.video_dest is not None:
            video_folder = os.path.split(self.video_dest)[0]
            if not os.path.exists(video_folder):
                os.makedirs(video_folder)
            if (not os.path.exists(self.video_dest)) or force:
                s = self.compose_video_string()
                print(s)
                result=subprocess.run(s, shell=True, capture_output=True)
            else:
                print('video exists: ',self.video_dest)
        if self.thumb_dest is not None:
            thumb_folder = os.path.split(self.thumb_dest)[0]
            if not os.path.exists(thumb_folder):
                os.makedirs(thumb_folder)
            if (not os.path.exists(self.thumb_dest)) or force:
                s = self.compose_thumb_string()
                print(s)
                result=subprocess.run(s, shell=True, capture_output=True)
            else:
                print('thumb exists: ',self.thumb_dest)

        

def clean_path(path_in):
    path_out = os.path.normpath(os.path.abspath(os.path.expanduser(path_in)))
    return path_out

def load_yaml(path):
    with open(path,'rb') as f:
        t = f.read().decode('utf-8-sig')
    my_yaml = yaml.load(t,Loader=yaml.Loader)
    # print(my_yaml)
    return my_yaml
    
# def load_movie(item):

    
                
if __name__=='__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('path',metavar='path',type=str,help='path', default = '*.mp4')
    # parser.add_argument('-p','--path',dest='path',default = '*.mp4')
    # parser.add_argument('-c','--config',dest='config',default = None)
    # parser.add_argument('-f','--filetype',dest='filetypes',default = 'mp4')
    # parser.add_argument('-t','--thumbs',dest='thumbs',action='store_true', default = None)
    parser.add_argument('-t','--thumb_path',dest='thumb_path',default = None)
    parser.add_argument('-v','--video_path',dest='video_path',default = None)
    parser.add_argument('-q','--crf',dest='crf',default = None)
    parser.add_argument('-p','--preset',dest='preset',default = None)
    parser.add_argument('-f','--force',dest='force',action='store_true', default = None)
    # parser.add_argument('command',metavar='command',type=str,help='command', default = '')
    # parser.add_argument('--token',dest='token',default = None)
    args = parser.parse_args()
    print('path: ',args.path)
    # print('config: ',args.config)

    # thumbs = args.thumbs
    # print('thumbs: ',thumbs)
    # print('filetype: ',args.filetypes)
    thumb_path = args.thumb_path
    print('thumb_path: ',thumb_path)
    video_path= args.video_path
    print('video_path: ',video_path)
    
    if args.crf is not None:
        crf = int(args.crf)
    else:
        crf = None
    
    force = args.force or False
    # path = args.path
    # print('computed path: ',path)
    
    # filetypes = args.filetypes.split(',')
    files = glob.glob(args.path)
    # files = [clean_path(file) for file in files]
    print(yaml.dump(files))
    
    for item in files:
        if os.path.splitext(item)[1]=='.yaml':
            print('process yaml',item)
            my_yaml = load_yaml(item)
            for yaml_movie in my_yaml:
                movie = Movie.build_from_dict(yaml_movie,video_path = video_path,thumb_path = thumb_path,crf = crf,preset=args.preset)
                try:
                    movie.process(force=force)
                except FileNotFoundError:
                    print('file not found: ',yaml_movie)
        else:
            print('process video',item)
            movie = Movie(item,video_path = video_path,thumb_path = thumb_path,crf = crf,preset=args.preset)
            try:
                movie.process(force=force)
            except FileNotFoundError:
                print('file not found: ',item)
            