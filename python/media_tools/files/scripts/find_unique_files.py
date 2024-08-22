# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 23:49:30 2020

@author: danaukes
"""

import file_sorter.support as fus
import file_sorter.images as fui
import yaml
import os
import shutil

# should be done in a separate script if on a remote machine
# path1 = r'/home/danaukes/nas/photos/2021'
# path2 = r'/home/danaukes/nas/photos/2020'
# hash1 = fus.scan_list(path1,path2,directories_recursive=True,file_filter=fus.filter_none,hasher=fus.hash_filesize,directory_hashfile_name='hash_filesize.yaml')
# hash1.save(os.path.expanduser('~'),'size_remote.yaml')

with open(os.path.join(os.path.expanduser('~'),'size_remote.yaml')) as f:
    remote_compare1 = yaml.load(f,Loader=yaml.Loader)

path1 = r'C:\Users\danaukes\Desktop\Camera'
hash1 = fus.scan_list(path1,directories_recursive=True,file_filter=fus.filter_none,hasher=fus.hash_filesize,directory_hashfile_name='hash_filesize.yaml')
hash1.save(os.path.expanduser('~'),'size_local.yaml')

with open(os.path.join(os.path.expanduser('~'),'size_local.yaml')) as f:
    local_compare1 = yaml.load(f,Loader=yaml.Loader)

same_size_hashes = set(local_compare1.hashes).intersection(set(remote_compare1.hashes))

new_local_file_hashes1 = set(local_compare1.hashes).difference(set(same_size_hashes))
new_local_file_names1 = [filename for key in new_local_file_hashes1 for filename in local_compare1.hash_file_dict[key]]

local_files_to_check = [item for key in same_size_hashes for item in local_compare1.hash_file_dict[key]]
with open(os.path.join(os.path.expanduser('~'),'local_files_to_check.yaml'),'w') as f:
    yaml.dump(local_files_to_check,f)

# remote_files_to_check = [item for key in same_size_hashes for item in remote_compare1.hash_file_dict[key]]
# with open(os.path.join(os.path.expanduser('~'),'remote_files_to_check.yaml'),'w') as f:
#     yaml.dump(remote_files_to_check,f)
    
# with open(os.path.join(os.path.expanduser('~'),'remote_files_to_check.yaml')) as f:
#     remote_files_to_check = yaml.load(f,Loader = yaml.Loader)
# remote_compare2 = fus.scan_list(*remote_files_to_check,directories_recursive=False,file_filter = fus.filter_none,hasher=fus.hash_file)
# remote_compare2.save(os.path.expanduser('~'),'sha256_remote.yaml')

with open(os.path.join(os.path.expanduser('~'),'local_files_to_check.yaml')) as f:
    local_files_to_check = yaml.load(f,Loader = yaml.Loader)
local_compare2 = fus.scan_list(*local_files_to_check,directories_recursive=False,file_filter = fus.filter_none,hasher=fus.hash_file)
local_compare2.save(os.path.expanduser('~'),'sha256_local.yaml')

with open(os.path.join(os.path.expanduser('~'),'sha256_local.yaml')) as f:
    local_compare2 = yaml.load(f,Loader=yaml.Loader)
with open(os.path.join(os.path.expanduser('~'),'sha256_remote.yaml')) as f:
    remote_compare2 = yaml.load(f,Loader=yaml.Loader)


same_file_hashes = set(local_compare2.hashes).intersection(set(remote_compare2.hashes))
same_file_names = [filename for key in same_file_hashes for filename in remote_compare2.hash_file_dict[key]]

new_local_file_hashes2 = set(local_compare2.hashes).difference(set(same_file_hashes))
new_local_file_names2 = [filename for key in new_local_file_hashes2 for filename in local_compare2.hash_file_dict[key]]

new_local_file_names = list(set(new_local_file_names1+new_local_file_names2))

new_path = os.path.join(os.path.expanduser('~'),'Desktop','new')
if not os.path.exists(new_path):
    os.mkdir(new_path)
for filename in new_local_file_names:
    
    new_file = os.path.join(new_path,os.path.split(filename)[1])
    shutil.copy2(filename,new_file)
#     # os.rename(filename, new_file)
#     # os.remove(filename)
