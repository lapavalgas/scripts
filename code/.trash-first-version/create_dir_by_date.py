import os
import os.path
import time
from datetime import datetime

import shutil

folder = ".\\"

for file in os.listdir(folder):

    if os.path.isfile(file): # talvez precise comentar dependendo a versão do python

        if file != "create_dir_by_date.py":

            # LOCALIZA OS ARQUIVOS
            path = folder + file
            print("Name: " + file)

            # PEGA AS DATAS
            lastModifiedDateTime = time.ctime(os.path.getmtime(path))
            date_of_created = datetime.strptime(lastModifiedDateTime, "%a %b %d %H:%M:%S %Y") # Convert string to date format
            # print("Last modified year: {} , month: {} , day: {}".format(str(date_of_created.year),str(date_of_created.month),str(date_of_created.day)))

            # CRIA PADRAO DATAS DIRETORIOS
            prefix = "{}".format(str(date_of_created.year)) 
            if int(date_of_created.month) >= 10:
                prefix += "{}".format(str(date_of_created.month))
            else:
                prefix += "0{}".format(str(date_of_created.month))
                
            if int(date_of_created.day) >= 10:
                prefix += "{}".format(str(date_of_created.day))
            else:
                prefix += "0{}".format(str(date_of_created.day))
            prefix += "_"
            print (prefix)

            # # # CRIA OS DIRETORIOS
            try: 
                os.mkdir(folder+prefix)
            except OSError:
                print ("Creation of the directory %s failed" % path)
            else:
                print ("Successfully created the directory %s " % path)

            new_path = folder + "\\" + prefix + "\\" + file

            # MOVE OS ARQUIVOS
            shutil.move('{}'.format(path), '{}'.format(new_path))