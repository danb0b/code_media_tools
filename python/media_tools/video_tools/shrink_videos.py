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
import media_tools.video_tools.video_info as vi
import media_tools

class SubProcessFailure(Exception):
    pass

class MissingSource(Exception):
    pass

class Movie(object):
    
    _default_crf = 35
    _default_preset = 'ultrafast'
    _default_video_path = 'video'
    _default_thumb_path = 'thumb'
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
        video_dest = video_dest or self.build_video_dest(video_source,video_path or self._default_video_path)
        if video_dest is not None:
            self.video_dest = clean_path(video_dest)
        thumb_dest = thumb_dest or self.build_thumb_dest(video_source,thumb_path or self._default_thumb_path)
        if thumb_dest is not None:
            self.thumb_dest = clean_path(thumb_dest)
        self.crf = crf or Movie._default_crf
        self.preset = preset or Movie._default_preset
        self.start_time = start_time
        self.end_time = end_time
        self.thumb_time = thumb_time
        
        if (not os.path.exists(self.video_source)):
            raise(MissingSource(self.video_source))

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
            e = info.get_max_length2()
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
               
        s = 'ffmpeg -y -i "'+self.video_source+'" ' +st_string+et_string+ '-c:v libx264 -async 1 '+preset_string+crf_string+'"'+self.video_dest+'"'                    
        return s

    def compose_thumb_string(self):
        mt_string = '-ss {0:.3f} '.format(self.thumb_time or self.compute_thumb_time())
        
        s = 'ffmpeg -y '+mt_string+' -i "'+self.video_source+'" -q:v 1 -qscale:v 2 -frames:v 1 "'+self.thumb_dest+'"'
        return s
    
    def process(self,force=False,verbose=False,dry_run=False):
        if self.video_dest is not None:
            video_folder = os.path.split(self.video_dest)[0]
            if not os.path.exists(video_folder):
                if not dry_run:
                    os.makedirs(video_folder)
            if (not os.path.exists(self.video_dest)) or force:
                s = self.compose_video_string()
                if verbose:
                    print(s)
                if not dry_run:
                    result=subprocess.run(s, shell=True, capture_output=True)
            else:
                if verbose:
                    print('video exists: ',self.video_dest)
            if (not os.path.exists(self.video_dest)):
                if not dry_run:
                    raise(SubProcessFailure(self.video_dest))
        if self.thumb_dest is not None:
            try:
                thumb_folder = os.path.split(self.thumb_dest)[0]
                if not os.path.exists(thumb_folder):
                    if not dry_run:
                        os.makedirs(thumb_folder)
                if (not os.path.exists(self.thumb_dest)) or force:
                    s = self.compose_thumb_string()
                    if verbose:
                        print(s)
                    if not dry_run:
                        result=subprocess.run(s, shell=True, capture_output=True)
                else:
                    if verbose:
                        print('thumb exists: ',self.thumb_dest)
            except vi.NoVideoStream:
                raise
            if (not os.path.exists(self.video_dest)):

                if not dry_run:

                    raise(SubProcessFailure(self.thumb_Dest))
        

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
    parser.add_argument('--thumb_path',dest='thumb_path',default = None)
    parser.add_argument('--video_path',dest='video_path',default = None)
    parser.add_argument('-q','--crf',dest='crf',default = None)
    parser.add_argument('-p','--preset',dest='preset',default = None)
    parser.add_argument('-f','--force',dest='force',action='store_true', default = None)
    parser.add_argument('-r','--recursive',dest='recursive',action='store_true', default = None)
    parser.add_argument('-v','--verbose',dest='verbose',action='store_true', default = False)
    args = parser.parse_args()

    thumb_path = args.thumb_path
    video_path= args.video_path
    if args.verbose:
        print('thumb_path: ',thumb_path)
        print('video_path: ',video_path)
    
    if args.crf is not None:
        crf = int(args.crf)
    else:
        crf = None
    
    force = args.force or False
    
    path = clean_path(args.path)
    files = glob.glob(path,recursive=args.recursive)
    files = [item for item in files if os.path.splitext(item)[1][1:].lower() in (media_tools.video_filetypes+media_tools.yaml_filetypes)]
    
    if args.verbose:
        verbose = args.verbose
        print('path: ',path)
        print(yaml.dump(files))
    
    for item in files:
        if os.path.splitext(item)[1]=='.yaml' or os.path.splitext(item)[1]=='.yml':
            if args.verbose:
                print('process yaml',item)
            my_yaml = load_yaml(item)
            for yaml_movie in my_yaml:
                movie = Movie.build_from_dict(yaml_movie,video_path = video_path,thumb_path = thumb_path,crf = crf,preset=args.preset)
                try:
                    movie.process()
                except FileNotFoundError:
                    print('file not found: ',yaml_movie)
        else:
            if args.verbose:
                print('process video',item)
            movie = Movie(item,video_path = video_path,thumb_path = thumb_path,crf = crf,preset=args.preset)
            try:
                movie.process(force=force,verbose=args.verbose)
            except FileNotFoundError:
                print('file not found: ',item)
            
