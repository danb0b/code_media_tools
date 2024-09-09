#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 08:14:30 2022

@author: danaukes
"""
import re
import os

search_string=r'[!@#$%^&*<>?:{}|~`=\[\]\\;,/'+"\t\r']"


def eliminate_multiple_characters(string_in,char):
    l = len(string_in)
    l_last = l+1
    while l_last>l:
        string_in = string_in.replace(char+char,char)
        l_last = l
        l = len(string_in)
    return string_in
    
def slugify(string_in,max_len = 64):
    string_in = string_in[:]
    string_in = string_in.replace(' ','-')
    string_in = string_in.replace('/','-')
    string_in = string_in.lower()
    search = re.compile(search_string)    
    string_in = search.sub('',string_in)
    string_in = eliminate_multiple_characters(string_in, '-')
    string_in = eliminate_multiple_characters(string_in, '.')
    string_in = string_in[:max_len]
    string_in = string_in.lstrip('-').rstrip('-')
    return string_in

if __name__=='__main__':
    text = '---asdfa..sdfasdfasdfqiuoewrpqowirupqower,m.nxcv.zm,x;,../<>?][\\01980912837986!@#$!$#%@#%$^#$%&%#^&&%^*^&#@$%!#%!~``[];'
    
    print(slugify(text))
