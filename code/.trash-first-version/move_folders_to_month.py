import os
import os.path
import time
from datetime import datetime

import shutil   

folder = "E:/"

year = folder[len(folder)-5:len(folder)-1]

for file in os.listdir(folder):

    # if os.path.isfile(file): # talvez precise comentar dependendo a versão do python

        if file != "move_folders_to_month.py":

            # LOCALIZA OS ARQUIVOS

            print("Name: " + file)

            # IDENTIFICA O MÊS
            path = folder
            path_file = path + file

            month = file[4:6]

            if month[0] != "_":

                # MOVE OS ARQUIVOS

                if month == "01":
                    new_path = path + "{}{}_janeiro".format(year,month)
                    shutil.move('{}'.format(path_file), '{}'.format(new_path))

                if month == "02":
                    new_path = path + "{}{}_fevereiro".format(year,month)
                    shutil.move('{}'.format(path_file), '{}'.format(new_path))

                if month == "03":
                    new_path = path + "{}{}_marco".format(year,month)
                    shutil.move('{}'.format(path_file), '{}'.format(new_path))

                if month == "04":
                    new_path = path + "{}{}_abril".format(year,month)
                    shutil.move('{}'.format(path_file), '{}'.format(new_path))

                if month == "05":
                    new_path = path + "{}{}_maio".format(year,month)
                    shutil.move('{}'.format(path_file), '{}'.format(new_path))

                if month == "06":
                    new_path = path + "{}{}_junho".format(year,month)
                    shutil.move('{}'.format(path_file), '{}'.format(new_path))

                if month == "07":
                    new_path = path + "{}{}_julho".format(year,month)
                    shutil.move('{}'.format(path_file), '{}'.format(new_path))

                if month == "08":
                    new_path = path + "{}{}_agosto".format(year,month)
                    shutil.move('{}'.format(path_file), '{}'.format(new_path))

                if month == "09":
                    new_path = path + "{}{}_setembro".format(year,month)
                    shutil.move('{}'.format(path_file), '{}'.format(new_path))

                if month == "10":
                    new_path = path + "{}{}_outubro".format(year,month)
                    shutil.move('{}'.format(path_file), '{}'.format(new_path))

                if month == "11":
                    new_path = path + "{}{}_novembro".format(year,month)
                    shutil.move('{}'.format(path_file), '{}'.format(new_path))

                if month == "12":
                    new_path = path + "{}{}_dezembro".format(year,month)
                    shutil.move('{}'.format(path_file), '{}'.format(new_path))
