from pypdf import PdfWriter
import os
import shutil
import yaml
import argparse

# root='/media/dropbox_asu/classes/me473/course-folder/'
root = '/home/danaukes/Desktop/temp/course-folder/'
final = os.path.join(root,'final.pdf')

dummy = list(os.walk(root))

all_pdfs = []

for path,subdirs,files in os.walk(root):
    pdfs = [item for item in files if item.endswith('.pdf')]
    pdfs = [os.path.join(path,item) for item in pdfs]
    all_pdfs.extend(pdfs)

all_pdfs.sort()

s = yaml.dump(all_pdfs)
print(s)

merger = PdfWriter()



input1 = open(all_pdfs.pop(0), "rb")
inputs = [open(item, "rb") for item in all_pdfs]
# input2 = open("document2.pdf", "rb")
# input3 = open("document3.pdf", "rb")

# # Add the first 3 pages of input1 document to output
merger.append(fileobj=input1)

for ii,item in enumerate(inputs):
    merger.append(item)


# # Insert the first page of input2 into the output beginning after the second page

# # Append entire input3 document to the end of the output document
# merger.append(input3)

# # Write to an output PDF document
output = open(final, "wb")
merger.write(output)

# # Close file descriptors
merger.close()
output.close()

