# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 08:43:11 2020

@author: danaukes
"""

import yaml
import os
import sys
import glob
from file_sorter.support import HashFile
import file_sorter.support as fus
import matplotlib.pyplot as plt
plt.ion()

first_pass = fus.hash_filesize
first_pass_filename = 'hash_filesize.yaml'
second_pass = fus.hash_file
dry_run = False

duplicate_dir = r'Y:\2020\DCIM'
fus.scan_compare_dir(duplicate_dir, recursive=True,file_filter=fus.filter_none,hasher=first_pass,local_hashfile=first_pass_filename)
duplite_hashfiles = glob.glob(duplicate_dir+'/**/*.yaml',recursive=True)
dupes = HashFile({},{},[])
for file in duplite_hashfiles:
    new = HashFile.load(file)
    dupes.merge(new)
dupe_hashes= set(dupes.hashes)
    

# compare_dir = r'Y:\2020\2020-02-06 Australia'
# compare_dir = r'C:\Users\danaukes\Dropbox (Personal)\projects\2019-12-24 passport photos'
compare_dir = r'C:\Users\danaukes\Dropbox (Personal)\projects\2020-04-15 Garden Tour'
fus.scan_compare_dir(compare_dir, recursive=True,file_filter=fus.filter_none,hasher=first_pass,local_hashfile=first_pass_filename)
compare_hashfiles = glob.glob(compare_dir+'/**/*.yaml',recursive=True)
compares = HashFile({},{},[])
for file in compare_hashfiles:
    new = HashFile.load(file)
    compares.merge(new)
compare_hashes = set(compares.hashes)

same_hashes = compare_hashes.intersection(dupe_hashes)

# fig = plt.figure()
# plt.show()


same_hashes = list(same_hashes)

# compare_files2 = []
# for item in same_hashes:
    # compare_files2.extend(compares.hash_file_dict[item])
# compare2 = HashFile.build(fus.hash_filesize)

# direc1 = r'C:\Users\danaukes\Desktop\test'
# with open(direc1+'/same_hashes.yaml','w') as f:
#     yaml.dump(same_hashes)

for jj,item in enumerate(same_hashes):
    print(compares.hash_file_dict[item],dupes.hash_file_dict[item],)
    files = []
    if len(compares.hash_file_dict[item])==1:
        refitem = compares.hash_file_dict[item][0]
        refhash = second_pass(refitem)
        for item2 in dupes.hash_file_dict[item]:
            if second_pass(item2)==refhash:
                print('removing',item2)
                if not dry_run:
                    os.remove(item2)
#     files.extend(dupes.hash_file_dict[item])
#     files.extend(compares.hash_file_dict[item])
#     images = [item for item in files if os.path.splitext(item)[1] in ['.jpg']]
#     sizes = [os.path.getsize(item) for item in files]
#     print(sizes)
#     n = len(images)
#     for ii,i in enumerate(images):
#         ax = fig.add_subplot(1,n,ii+1)
#         im = plt.imread(i)
#         ax.imshow(im)
#     fig.canvas.draw()
#     # plt.draw()
#     # value = input('dup')
#     fig.savefig(direc1+'/{0:03.0f}'.format(jj)+'.png')
#     fig.clear()
    
# # for item in same_hashes:
# #     print(dupes.hash_file_dict[item])
# #     for file in dupes.hash_file_dict[item]: 
# #         os.remove(file)