# -*- coding: utf-8 -*-
"""
Created on Tue May 25 16:17:18 2021

@author: danaukes
"""

import media_tools.files.support as fus
import media_tools.files.images as fui
import yaml
import os
import shutil

with open(os.path.join(os.path.expanduser('~'),'remote_files_to_check.yaml')) as f:
    remote_files_to_check = yaml.load(f,Loader = yaml.Loader)
remote_compare2 = fus.scan_list(*remote_files_to_check,directories_recursive=False,file_filter = fus.filter_none,hasher=fus.hash_file)
remote_compare2.save(os.path.expanduser('~'),'sha256_remote.yaml')
