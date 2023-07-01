import os
import datetime
from PIL import Image 
from PIL.ExifTags import TAGS 

PATTERN_SLASH = '/'
PATTERN_DOT = '.'

DATE_TIME = 'DateTime'
DATE_TIME_ORIGINAL = 'DateTimeOriginal'

DIR = 'DIR'
DOC = 'DOC'
IMG = 'IMG'

PATTERN_DATETIME_EXIFTAGS = '%Y:%m:%d %H:%M:%S'

class Path:

    directory_path = str
    full_path = str
    is_file = bool
    file_name = str
    file_extension = str
    file_type = str 
    datetime_oldest = datetime.datetime

    @classmethod
    def __is_file__(self, path, file_extension):
        return os.path.isfile(path) or file_extension.__contains__(PATTERN_DOT)

    @classmethod
    def __validate_file_extension_as_image__(cls, file_extension):
        if file_extension == None:
            return False
        return file_extension.lower().endswith(('.png', '.jpg', '.JPG', '.jpeg', '.tiff', '.bmp', '.gif'))
    
    @classmethod
    def get_metadatas(clas, full_path):
        datetime_metadatas = []
        datetime_metadatas.append(datetime.datetime.fromtimestamp(os.path.getatime(full_path)))
        datetime_metadatas.append(datetime.datetime.fromtimestamp(os.path.getctime(full_path)))
        datetime_metadatas.append(datetime.datetime.fromtimestamp(os.path.getmtime(full_path)))
        return datetime_metadatas         

    @classmethod
    def get_image_metadata(cls, full_path):
        datetime_metadatas = []
        metadatas = {}
        try: 
          image = Image.open(full_path)
          for tag, value in image._getexif().items():
               if tag in TAGS:
                    metadatas[TAGS[tag]] = value
          if metadatas.get('DateTime') != None:
              datetime_metadatas.append(datetime.datetime.strptime(metadatas.get('DateTime'), PATTERN_DATETIME_EXIFTAGS))
          if metadatas.get('DateTimeOriginal') != None:
              datetime_metadatas.append(datetime.datetime.strptime(metadatas.get('DateTimeOriginal'), PATTERN_DATETIME_EXIFTAGS))
          # # # The 'DateTimeDigitized' can be a date before than the photo has taken \ weired!
          # if metadatas.get('DateTimeDigitized') != None:
          #     datetime_metadatas.append(datetime.datetime.strptime(metadatas.get('DateTimeDigitized'), PATTERN_DATETIME_EXIFTAGS))
          datetime_metadatas.append(datetime.datetime.fromtimestamp(os.path.getatime(full_path)))
          datetime_metadatas.append(datetime.datetime.fromtimestamp(os.path.getctime(full_path)))
          datetime_metadatas.append(datetime.datetime.fromtimestamp(os.path.getmtime(full_path)))
          return datetime_metadatas
        except:
          return Path.get_metadatas(full_path)

    def __init__(self, path, USE_EXIFTAGS) -> None:
        path_and_file_name, file_extension = os.path.splitext(path)
        if path == 'C:/Users/lapav/Downloads/teste nova classe/CDs/fotos/2000-2009/2002/2002012_dezembro/1.JPG':
            print('hello')
        if Path.__is_file__(path, file_extension):
            self.is_file = True
            self.file_extension = file_extension.lower()
            self.file_type = IMG if Path.__validate_file_extension_as_image__(self.file_extension) else DOC
            full_path_list = path_and_file_name.split(PATTERN_SLASH)
            self.file_name = full_path_list.pop(-1)
            self.directory_path = '/'.join(full_path_list)
            self.full_path = f'{self.directory_path}/{self.file_name}{file_extension}'
            if USE_EXIFTAGS and Path.__validate_file_extension_as_image__(self.file_extension):
                datetime_metadatas = Path.get_image_metadata(self.full_path)
            else:   
               datetime_metadatas = Path.get_metadatas(self.full_path)
            datetime_metadatas.sort()
            self.datetime_oldest = datetime_metadatas[0]
        else:
            self.is_file = False
            self.directory_path = path
            self.full_path = path
            self.file_type = DIR

    def get_year(self):
         return self.datetime_oldest.year

    def get_year_range(self):
         if self.get_year() <= 1999:
              return '1988-1999'
         if self.get_year() >= 2000 and self.get_year() <= 2009:
              return '2000-2009'
         if self.get_year() >= 2010 and self.get_year() <= 2019:
              return '2010-2019'
         if self.get_year() >= 2020 and self.get_year() <= 2029:
              return '2020-2029'
    
    def get_month(self):
         return self.datetime_oldest.month
    
    def get_month_in_full(self):
         if (self.get_month()) == 1:
              return 'janeiro'
         if (self.get_month()) == 2:
              return 'fevereiro'
         if (self.get_month()) == 3:
              return 'marco'
         if (self.get_month()) == 4:
              return 'abril'
         if (self.get_month()) == 5:
              return 'maio'
         if (self.get_month()) == 6:
              return 'junho'
         if (self.get_month()) == 7:
              return 'julho'
         if (self.get_month()) == 8:
              return 'agosto'
         if (self.get_month()) == 9:
              return 'setembro'
         if (self.get_month()) == 10:
              return 'outubro'
         if (self.get_month()) == 11:
              return 'novembro'
         if (self.get_month()) == 12:
              return 'dezembro'

    def destine_full_path(self, end_directory):
        if Path.__validate_file_extension_as_image__(self.file_extension):
            if self.get_month() <= 9: 
                return f'{end_directory}/fotos/{self.get_year_range()}/{self.get_year()}/{self.get_year()}0{self.get_month()}_{self.get_month_in_full()}/{self.file_name}{self.file_extension}'
            else:
                return f'{end_directory}/fotos/{self.get_year_range()}/{self.get_year()}/{self.get_year()}{self.get_month()}_{self.get_month_in_full()}/{self.file_name}{self.file_extension}'
        else:
            if self.get_month() <= 9:
                return f'{end_directory}/docs/{self.get_year()}/{self.get_year()}0{self.get_month()}_{self.get_month_in_full()}/{self.file_name}{self.file_extension}' 
            else:
                return f'{end_directory}/docs/{self.get_year()}/{self.get_year()}{self.get_month()}_{self.get_month_in_full()}/{self.file_name}{self.file_extension}'

    def destine_directory(self, end_directory):
        if Path.__validate_file_extension_as_image__(self.file_extension):
            if self.get_month() <= 9:
                return f'{end_directory}/fotos/{self.get_year_range()}/{self.get_year()}/{self.get_year()}0{self.get_month()}_{self.get_month_in_full()}'
            else:
                return f'{end_directory}/fotos/{self.get_year_range()}/{self.get_year()}/{self.get_year()}{self.get_month()}_{self.get_month_in_full()}'
        else:
            if self.get_month() <= 9:
                return f'{end_directory}/docs/{self.get_year()}/{self.get_year()}0{self.get_month()}_{self.get_month_in_full()}' 
            else:
                return f'{end_directory}/docs/{self.get_year()}/{self.get_year()}{self.get_month()}_{self.get_month_in_full()}' 