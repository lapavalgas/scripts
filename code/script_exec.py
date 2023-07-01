import Path as __create_path_instance
import os
import shutil   
from datetime import datetime

START_DIRECTORY = 'C:/Users/lapav/Downloads/teste nova classe/CDs'
END_DIRECTORY = 'C:/Users/lapav/Downloads/teste nova classe'

LIST_DIRECTORIES = []
LIST_IMAGES = []
LIST_DOCS = []

LIST_EXCEPTIONS_TO_CREATE_DIR = []
LIST_EXCEPTIONS_TO_MOVE_FILE = []
EXCEPTION_ALREADY_EXISTS = 'ALREADY EXISTS'
EXCEPTION_NEED_ATTENTION = 'NEED ATTENTION'

LIST_LOGS = []

DATE_TIME_FOR_EXCEPTIONS = "%d/%m/%Y %H:%M:%S"
DATE_TIME_FOR_FILE_NAME = "%Y%m%d%H%M"

DIR = 'DIR'
DOC = 'DOC'
IMG = 'IMG'


def wrtie_log(file_name, list):
    f = open(file_name, 'w')
    for log in list:
        f.write(log)
        f.write('\n')
    f.close()

def get_datetime(STRFTIME_PATTERN):
    now = datetime.now()
    dt_string = now.strftime(STRFTIME_PATTERN)
    return dt_string

def log(str):
    LIST_LOGS.append(str)

def log_exception(exceptions_list, str):
    exceptions_list.append(str)

# # # # # # # # # # # #
#   S E T E P  -  1   # 
# # # # # # # # # # # #

def mapper_path_to_object(directory, str_path):
    object_path = __create_path_instance.Path(f'{directory}/{str_path}')
    if object_path.file_type == DIR:
        LIST_DIRECTORIES.append(object_path.full_path)
    if object_path.file_type == DOC:
        LIST_DOCS.append(object_path)
    if object_path.file_type == IMG:
        LIST_IMAGES.append(object_path)

def rabbit_hole_read_directories_recursively(): 
    if not LIST_DIRECTORIES: # the rabbit hole exit
        return
    for directory in LIST_DIRECTORIES:
        for file_or_directory_path in os.listdir(directory):
            mapper_path_to_object(directory, file_or_directory_path)
        LIST_DIRECTORIES.pop(LIST_DIRECTORIES.index(directory))
    rabbit_hole_read_directories_recursively() # the rabbit hole

# START HERE #

for file_or_directory_path in os.listdir(START_DIRECTORY):
    mapper_path_to_object(START_DIRECTORY, file_or_directory_path)

rabbit_hole_read_directories_recursively()

# # # # # # # # # # # #
#   S E T E P  -  2   # 
# # # # # # # # # # # #

def create_dir_exception_str(destine_path, error_type):
    return f'{get_datetime(DATE_TIME_FOR_EXCEPTIONS)} - Creation of the directory FAILED: \t{destine_path} \t-\t{error_type}'

def create_directories(object_path):
    try:
        directory_path = object_path.destine_directory(END_DIRECTORY)
        os.makedirs(directory_path)
    except OSError: #
        log_exception(LIST_EXCEPTIONS_TO_CREATE_DIR, create_dir_exception_str(directory_path, EXCEPTION_ALREADY_EXISTS)) if os.path.isdir(directory_path) else log_exception(LIST_EXCEPTIONS_TO_CREATE_DIR, create_dir_exception_str(directory_path, EXCEPTION_NEED_ATTENTION))

for object_path in LIST_DOCS:
    create_directories(object_path)

for object_path in LIST_IMAGES:
    create_directories(object_path)

exceptions_create_dir_log_file_name = f'{get_datetime(DATE_TIME_FOR_FILE_NAME)}_exceptions_to_create_directory_log.txt'

wrtie_log(exceptions_create_dir_log_file_name, LIST_EXCEPTIONS_TO_CREATE_DIR)

# # # # # # # # # # # #
#   S E T E P  -  3   # 
# # # # # # # # # # # #

def move_file_exception_str(object_path):
    return f'{get_datetime(DATE_TIME_FOR_EXCEPTIONS)} - Extension: {object_path.file_extension}\t- FAILED to moving \t{object_path.full_path}\n \t\t\t\t\t\t{object_path.destine_full_path(END_DIRECTORY)}\nFAILED -\tNEED ATTENTION\n'

def move_file_to_destine(object_path):
    old_path = object_path.full_path
    destine_path = object_path.destine_full_path(END_DIRECTORY)
    try:
        shutil.move(old_path, destine_path)
    except:
        log_exception(LIST_EXCEPTIONS_TO_MOVE_FILE, move_file_exception_str(object_path))

for object_path in LIST_DOCS:
    move_file_to_destine(object_path)

for object_path in LIST_IMAGES:
    move_file_to_destine(object_path)
    
exceptions_move_file_log_file_name = f'{get_datetime(DATE_TIME_FOR_FILE_NAME)}_exceptions_to_move_file_log.txt'

wrtie_log(exceptions_create_dir_log_file_name, LIST_EXCEPTIONS_TO_CREATE_DIR)