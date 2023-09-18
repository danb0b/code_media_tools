import PIL
from PIL import Image,  ExifTags
import os
from media_tools.video_tools.shrink_videos import Movie


def get_rotate_amount(exif):
    try:
        tags_inverse = dict([(value.lower(), key)
                            for key, value in ExifTags.TAGS.items()])
        orientation_key = tags_inverse['orientation']

        # exif = image.getexif()

        if exif[orientation_key] == 3:
            rotate_amount = 180
        elif exif[orientation_key] == 6:
            rotate_amount = 270
        elif exif[orientation_key] == 8:
            rotate_amount = 90
        else:
            rotate_amount = 0

        return rotate_amount

    except (AttributeError, KeyError, IndexError):
        return 0


def process_image(item, folder, newfolder, size, size_non_thumbnail, bad_photos,dry_run=False):

    if not dry_run:
        from_file_name = os.path.join(folder, item)
        try:
            i = Image.open(from_file_name)
            e = i.getexif()
            r = get_rotate_amount(e)
            non_i = i.copy()
            if r in (0, 180):
                i.thumbnail(size)
                non_i.thumbnail(size_non_thumbnail)
            else:
                i.thumbnail(size[::-1])
                non_i.thumbnail(size_non_thumbnail[::-1])
            if r != 0:
                i = i.rotate(r, expand=True)
                non_i = non_i.rotate(r, expand=True)
            a, b = os.path.splitext(item)
            i.save(os.path.join(newfolder, a+'_thumb'+b))
            non_i.save(os.path.join(newfolder, item))
        #     # i.show()
        #     # display(i)
        except PIL.UnidentifiedImageError:
            bad_photos.append(from_file_name)


def process_video(item, folder, newfolder, crf, preset, rebuild_from_scratch, verbose, size,dry_run=False):
    movie = Movie(os.path.join(folder, item), video_path=newfolder,thumb_path=newfolder, crf=crf, preset=preset)
    try:
        movie.process(force=rebuild_from_scratch, verbose=verbose,dry_run=dry_run)
        if not dry_run:
            i = Image.open(movie.thumb_dest)
            i.thumbnail(size)
            thumb = os.path.splitext(movie.thumb_dest)[0]+'_thumb.png'
            i.save(thumb)
    except FileNotFoundError:
        print('file not found: ', item)
