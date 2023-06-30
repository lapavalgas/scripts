### lib para extrair metadatas 
# pip3 install Pillow 
### imports para extrair metadatas
from PIL import Image
from PIL.ExifTags import TAGS

import os
import os.path
import time
from datetime import datetime
import subprocess 

import shutil   

def check_file_extension(file_extension):
    if not file_extension == ".mp4" and not file_extension == ".pdf" and not file_extension == ".JPEG" and not file_extension == ".JPG" and not file_extension == ".db":
        return True
    return False

def extract_image_metadatas(image_path):
    metadata = []
    image_path = folder+file
    image = Image.open(image_path)
    info_dict = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    # print(info_dict)
    exifdata = image.getexif()
    # iterating over all EXIF data fields
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            data = data.decode()
        # print(f"{tag:25}: {data}")
        metadata.append(f"{tag:25}: {data}")
    return metadata

# # # --------------- script starts here --------------- # # #

folder = "E:/"

year = folder[len(folder)-15:len(folder)-11]

for file in os.listdir(folder):
    
    file_name, file_extension = os.path.splitext(folder+file)

    image_path = folder+file

    all_files_metadatas = []

    if file_extension == ".jpg" or file_extension == ".png":
        all_files_metadatas.append(extract_image_metadatas(image_path))

    for line in all_files_metadatas:
        if line[0:8] == "DateTime":
            # print(line)
            image_shottaken_year = line[27:31]
            # print(image_shottaken_year)
            if not year == image_shottaken_year:
                print(f'not same {year} !== {image_shottaken_year}')