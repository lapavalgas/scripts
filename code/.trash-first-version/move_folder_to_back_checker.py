import os
import os.path
import time
from datetime import datetime

import shutil   

path = "E:/"

for folder in os.listdir(path):

    if not os.path.isfile(path+folder):

        for file in os.listdir(path+folder):
  
            shutil.move('{}'.format(path+folder+"/"+file), '{}'.format(path)) 