# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 12:59:11 2021

@author: danaukes
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
    
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/75.0'}


def cleanpath(path):
    return os.path.normpath(os.path.abspath(os.path.expanduser(path)))

webaddresses = [
    'https://danaukes.com/bookmarks/asu.html',
    'https://danaukes.com/bookmarks/courses-and-classrooms.html',
    'https://danaukes.com/bookmarks/guis-and-qt.html',
    'https://danaukes.com/bookmarks/idealab.html',
    'https://danaukes.com/bookmarks/markdown-pandoc-and-more.html',
    'https://danaukes.com/bookmarks/parts-and-materials-for-robotics.html',
    'https://danaukes.com/bookmarks/personal.html',
    'https://danaukes.com/bookmarks/programming.html',
    'https://danaukes.com/bookmarks/python.html',
    'https://danaukes.com/bookmarks/raspberry-pi.html',
    'https://danaukes.com/bookmarks/robotics-topics.html',
    'https://danaukes.com/bookmarks/unsorted.html',
    'https://danaukes.com/bookmarks/web-development.html',
    'https://danaukes.com/bookmarks/ubuntu-and-linux.html',
    ]
#%%
import yaml
s='''
- asu.md
- courses-and-classrooms.md
- guis-and-qt.md
- idealab.md
- markdown-pandoc-and-more.md
- parts-and-materials-for-robotics.md
- personal.md
- programming.md
- python.md
- raspberry-pi.md
- robotics-topics.md
- ubuntu-and-linux.md
- unsorted.md
- web-development.md
'''
mdfiles = yaml.load(s,Loader = yaml.Loader)
mdfiles = [os.path.join(r'C:\Users\danaukes\websites\danb0b.github.io\bookmarks',item) for item in mdfiles]
#%%
if __name__=='__main__':
    for webaddress,mdfile in zip(webaddresses,mdfiles):
        path = cleanpath(os.curdir)
        # print(path)
        # webaddress = sys.argv[1]
        page = requests.get(webaddress,headers=headers)
        print(page.status_code)
        # html = page.text.encode('utf-8')
        # print(html)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.findAll('a')
        # print(links)
        urls = [link.attrs['href'] for link in links]
    
        responses = []
        for ii,url in enumerate(urls):
            try:
                response = requests.get(url, headers=headers, timeout=5)
                print('{0:3.0f} / {1:3.0f}, '.format(ii+1,len(links)),response)
                responses.append(response)
            # except requests.exceptions.MissingSchema as e:
            #     print('{0:3.0f} / {1:3.0f}, '.format(ii+1,len(links)),e)
            #     responses.append(e)
            # except requests.exceptions.ReadTimeout as e:
            #     print('{0:3.0f} / {1:3.0f}, '.format(ii+1,len(links)),e)
            #     responses.append(e)
            # except requests.exceptions.ConnectTimeout as e:
            #     print('{0:3.0f} / {1:3.0f}, '.format(ii+1,len(links)),e)
            #     responses.append(e)
            except Exception as e:        
                print('{0:3.0f} / {1:3.0f}, '.format(ii+1,len(links)),e)
                responses.append(e)
    # %%    
        to_remove = []
        to_check= []
        is_ok = []
        to_replace = []
        
    
        def ok(link,url,response):
            if url!=response.url:
                to_replace.append((url,response.url))
            else:
                is_ok.append(url)
        def replace(link,url,response):
            to_replace.append((url,''))
        def remove(link,url,response):
            to_remove.append(url)
        def check(link,url,response):
            to_check.append(url)
    
        code_action = {
            200: ok,
            403: check,
            404: remove,
            410: remove,
            500: remove,
            503: remove,
            301: replace,
            302: replace
            }
    
    # %%
        for link,url,response in zip(links,urls,responses):
            
            if isinstance(response, Exception):
                # if isinstance(response, requests.exceptions.InvalidURL):
                    # pass
                # else:
                to_remove.append(url)
            else:
                try:
                    code_action[response.status_code](link,url,response)
                except KeyError as e:
                    print(e,url,response)
    # %%
        results = {}
        results['to_remove'] = to_remove
        results['to_check'] = to_check
        results['is_ok'] = is_ok
        results['to_replace'] = to_replace
        
        # import yaml
        # with open(os.path.join(os.path.curdir,'url_fix.yaml'),'w') as f:
            # yaml.dump(results,f)
                
            
    # %%
        # mdfile = r'C:\Users\danaukes\websites\danb0b.github.io\bookmarks\programming.md'        
        with open(mdfile) as f:
            s = f.read()
        for str_from,str_to in to_replace:
            s=s.replace(str_from, str_to)
        rows = s.split('\n')
        newrows = []
        for row in rows:
            delete = False
            for item in to_remove:
                if item in row:
                    if item.startswith('http'):
                        delete = True
            if not delete:
                newrows.append(row)
        s = '\n'.join(newrows)
        with open(mdfile,'w') as f:
            f.write(s)
                