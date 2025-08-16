from PIL import Image 
import os
import glob

source_folder = '~/repos/publishing/book_flexible_robotics/book_extract'

source_folder=os.path.expanduser(source_folder)
source_folder=os.path.normpath(source_folder)

watermark_path = source_folder+'/../watermark.png'
pdf_path = source_folder+'/merge.pdf'

wm=Image.open(watermark_path)
wm=wm.rotate(45,expand=True)
wm = wm.resize((wm.size[0]*2,wm.size[1]*2),Image.Resampling.BILINEAR )
wmsize = wm.size


files = glob.glob(source_folder+"/*.png")
files.sort()
print(files)

images = []
for file in files:
    images.append(Image.open(file))

for image in images:
    imsize = image.size
    immove = (int((imsize[0]-wmsize[0])/2),int((imsize[1]-wmsize[1])/2))
    Image.Image.paste(image,wm,immove,wm)

images[0].save(
     pdf_path, "PDF" ,resolution=96.0, save_all=True, append_images=images[1:]
)