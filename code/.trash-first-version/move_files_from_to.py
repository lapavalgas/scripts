import os
import os.path
import time
from datetime import datetime

import shutil

script_work_local = "C:\\Users\\"

work_year = "2017"

for folder in os.listdir(script_work_local):

    if folder[4:6] == "01": 
        old_path = script_work_local + folder
        new_path = script_work_local + work_year + "01_janeiro"
        shutil.move(old_path, new_path)
    if folder[4:6] == "02": 
        old_path = script_work_local + folder
        new_path = work_year + "02_fevereiro"
        shutil.move(old_path, new_path)
    if folder[4:6] == "03": 
        old_path = script_work_local + folder
        new_path = work_year + "03_marco"
        shutil.move(old_path, new_path)
    if folder[4:6] == "04": 
        old_path = script_work_local + folder
        new_path = work_year + "04_abril"
        shutil.move(old_path, new_path)
    if folder[4:6] == "05": 
        old_path = script_work_local + folder
        new_path = work_year + "05_maio"
        shutil.move(old_path, new_path)
    if folder[4:6] == "06": 
        old_path = script_work_local + folder
        new_path = work_year + "06_junho"
        shutil.move(old_path, new_path)
    if folder[4:6] == "07": 
        old_path = script_work_local + folder
        new_path = work_year + "07_julho"
        shutil.move(old_path, new_path)
    if folder[4:6] == "08": 
        old_path = script_work_local + folder
        new_path = work_year + "08_agosto"
        shutil.move(old_path, new_path)
    if folder[4:6] == "08": 
        old_path = script_work_local + folder
        new_path = work_year + "08_agosto"
        shutil.move(old_path, new_path)
    if folder[4:6] == "09": 
        old_path = script_work_local + folder
        new_path = work_year + "09_setembro"
        shutil.move(old_path, new_path)
    if folder[4:6] == "10": 
        old_path = script_work_local + folder
        new_path = work_year + "10_outubro"
        shutil.move(old_path, new_path)
    if folder[4:6] == "11": 
        old_path = script_work_local + folder
        new_path = work_year + "11_novembro"
        shutil.move(old_path, new_path)
    if folder[4:6] == "12": 
        old_path = script_work_local + folder
        new_path = work_year + "12_dezembro"
        shutil.move(old_path, new_path)
