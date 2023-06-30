import os
import os.path
import time
from datetime import datetime

import shutil

input = "2023"

script_work_local = "E:/~temp/"

for folder in os.listdir(script_work_local):

    local_path = script_work_local
    folder_path = script_work_local + folder
    folder_old_name = folder_path 
    folder_new_name = local_path + input + folder

    if (folder != "~~temp"):

        if (folder != "input_year.py"):
        
            os.rename(folder_old_name, folder_new_name)