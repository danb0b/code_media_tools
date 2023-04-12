filename = '/home/danaukes/Downloads/22-3481_02_MS.pdf'

from pypdf import PdfReader

reader = PdfReader(filename)
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()
text = text.replace('\n',' ')
words = [item for item in text.split(' ')]

import re

p = re.compile('\W([a-zA-Z]*)\W*')

words2 = []
for word in words 
    result = p.search(word)
    words2.append(result.groups()[0])