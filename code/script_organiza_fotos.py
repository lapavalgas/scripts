import file_and_dir_path_class as FILE_DATA
import os
import shutil   
from datetime import datetime

START_DIRECTORY = 'C:/Users/'
END_DIRECTORY = 'C:/Users/'

CHILD_DIRECTORY_LIST = []
PATH_IMAGE_LIST = []
PATH_ANY_DOC_LIST = []

FILE_EXTENSION_LIST = []

EXCEPTION_LIST_CREATE_DIR = []
EXCEPTION_LIST_MOVE_FILE = []

def wrtie_exceptions(file_name, list):
    f = open(file_name, 'w')
    for error in list:
        f.write(error)
        f.write('\n')
    f.close()

def getDateTime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string
# # # # # # # # # # # # # # # # # # # # # # # # # # #
# S E T E P  -  1 # # BUSCA ARQUIVOS NOS DIRETÓRIOS #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

def parse_directory_files(directory, str_path):
    path = FILE_DATA.Path(f'{directory}/{str_path}')
    if not path.is_file:
        CHILD_DIRECTORY_LIST.append(path.full_path)
    if path.is_file:
        if path.__validate_file_extension__():
            PATH_IMAGE_LIST.append(path)
        else:
            PATH_ANY_DOC_LIST.append(path)

def get_inside_the_children_node():
    if not CHILD_DIRECTORY_LIST:
        return
    for str_child_path in CHILD_DIRECTORY_LIST:
        for str_path in os.listdir(str_child_path):
            parse_directory_files(str_child_path, str_path)
        CHILD_DIRECTORY_LIST.pop(CHILD_DIRECTORY_LIST.index(str_child_path))
    get_inside_the_children_node()

for str_path in os.listdir(START_DIRECTORY):
    parse_directory_files(START_DIRECTORY, str_path)

get_inside_the_children_node()

# print(len(CHILD_DIRECTORY_LIST))
# print(len(PATH_IMAGE_LIST))
# print(len(PATH_ANY_DOC_LIST))

# # # # # # # # # # # # # # # # # # # # # # # # # # #
# S E T E P  -  1 # # CRIA PASTAS E SUBPASTAS       #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

def create_dirs(path):
    try:
        dir_path = path.know_the_way_directory_path(END_DIRECTORY)
        os.makedirs(dir_path)
    except OSError:
        if os.path.isdir(dir_path):
            EXCEPTION_LIST_CREATE_DIR.append(f'{getDateTime()} - Creation of the directory FAILED: \t{dir_path} \t-\tALREADY EXISTS')
        else:
            EXCEPTION_LIST_CREATE_DIR.append(f'{getDateTime()} - Creation of the directory FAILED: \t{dir_path} \t-\tNEED ATTENTION')
    else:
        # print("Successfully created the directory %s " % path)
        pass

for path in PATH_ANY_DOC_LIST:
    create_dirs(path)

for path in PATH_IMAGE_LIST:
    create_dirs(path)

wrtie_exceptions('excepetion_list_create_dir.txt', EXCEPTION_LIST_CREATE_DIR)

# # # # # # # # # # # # # # # # # # # # # # # # # # #
# S E T E P  -  1 # # MOVE OS ARQUIVOS              #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

def move_to_dirs(path):
    old_path = path.full_path
    new_path = path.know_the_way(END_DIRECTORY)
    try:
        pass
        shutil.move(old_path, new_path)
    except:
        EXCEPTION_LIST_MOVE_FILE.append(f'{getDateTime()} - Extension: {path.file_extension}\t- FAILED to moving \t{old_path}\n \t\t\t\t\t\t{new_path}\nFAILED -\tNEED ATTENTION\n')
        # debug
        # neo_path = FILE_DATA.Path(old_path)
    else:
        # print("Successfully created the directory %s " % path)
        pass

for path in PATH_ANY_DOC_LIST:
    move_to_dirs(path)

for path in PATH_IMAGE_LIST:
    move_to_dirs(path)

wrtie_exceptions('excepetion_list_move_file.txt', EXCEPTION_LIST_MOVE_FILE)