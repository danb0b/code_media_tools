from PIL import Image 
import os
import glob
import argparse

def merge(source_folder,watermark_path=None):

    source_folder=os.path.normpath(os.path.expanduser(source_folder))

    pdf_path = source_folder+'/merge.pdf'

    if watermark_path is not None:
        wm=Image.open(watermark_path)
        wm=wm.rotate(45,expand=True)
        wm = wm.resize((wm.size[0]*2,wm.size[1]*2),Image.Resampling.BILINEAR )
        wmsize = wm.size


    files = []
    files.extend(glob.glob(source_folder+"/*.png"))
    files.extend(glob.glob(source_folder+"/*.jpg"))
    files.sort()
    print(files)

    images = []
    for file in files:
        images.append(Image.open(file))

    if watermark_path is not None:
        for image in images:
            imsize = image.size
            immove = (int((imsize[0]-wmsize[0])/2),int((imsize[1]-wmsize[1])/2))
            Image.Image.paste(image,wm,immove,wm)

    images[0].save(
        pdf_path, "PDF" ,resolution=96.0, save_all=True, append_images=images[1:]
    )

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w','--watermark',dest='watermark',metavar='watermark',default=None)
    parser.add_argument('path',metavar='path',type=str,help='path', default = None)

    # source_folder = '~/repos/publishing/book_flexible_robotics/book_extract'
    # watermark_path = source_folder+'/../watermark.png'
    args = parser.parse_args()

    print(args.path,args.watermark)

    merge(args.path,args.watermark)
