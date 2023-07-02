import os, re
import datetime
from datetime import date
from PIL import Image, ExifTags 
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
    def __validate_file_extension_as_video__(cls, file_extension):
        if file_extension == None:
            return False
        return file_extension.lower().endswith(('.mp4', '.mov', '.wmv', '.avi', 'mpeg', 'mpeg-2', '.mkv', '.flv', '.f4v', '.swf'))
    

    @classmethod
    def __validate_file_extension_as_photo__(cls, file_extension):
        if Path.__validate_file_extension_as_image__(file_extension) or Path.__validate_file_extension_as_video__(file_extension):
            return True
        return False
    
    @classmethod
    def get_datetime_metadatas(clas, full_path):
        datetime_metadatas = []
        datetime_metadatas.append(datetime.datetime.fromtimestamp(os.path.getatime(full_path)))
        datetime_metadatas.append(datetime.datetime.fromtimestamp(os.path.getctime(full_path)))
        datetime_metadatas.append(datetime.datetime.fromtimestamp(os.path.getmtime(full_path)))
        return datetime_metadatas         

    @classmethod
    def get_datatime_from_exif(cls, datetime_str):
        if not str is None:
          try:
               date_str, time_str = datetime_str.split(' ')
               hour_str = time_str[:2]
               hour_str = '23' if hour_str == '24' else hour_str
               corrected_datetime_str = f'{date_str} {hour_str}{time_str[2:]}'
               return datetime.datetime.strptime(corrected_datetime_str, PATTERN_DATETIME_EXIFTAGS)
          except:
               pass

    @classmethod 
    def extract_datetime_from_file_name(cls, nome_arquivo):
     # TODO: can implement a list of patterns to test, better than pick randomly by regex
     filename_datatime_pattern = r'(\d{4})(\d{2})(\d{2})'
     match = re.search(filename_datatime_pattern, nome_arquivo)
     if match:
          year = int(match.group(1))
          month = int(match.group(2))
          day = int(match.group(3))
          current_year = date.today().year
          if year < 2000 or year > current_year:
               return None
          if year >= 13:
              return None 
          if year >= 31:
              return None
          try:
               data = datetime.datetime(year, month, day)
               return data
          except ValueError:
               if month > 12:
                    data = datetime.datetime(year, month, 1)
                    return data
               else:
                    data = datetime.datetime(year, 1, 1)
                    return data
     else:
          return None

    @classmethod
    def get_the_file_name_datetime_better_than_metadatas(cls, file_name, oldest_datetime):
        file_name_datetime = Path.extract_datetime_from_file_name(file_name)
        if file_name_datetime == None:
          return oldest_datetime
        return file_name_datetime if file_name_datetime < oldest_datetime else oldest_datetime

    @classmethod #
    def get_metadata_exiftags(cls, full_path):
          datetime_metadatas = Path.get_datetime_metadatas(full_path)
          metadatas = {}
          try: 
               image = Image.open(full_path)
               for tag, value in image.getexif().items():
                    if tag in TAGS:
                         metadatas[TAGS[tag]] = value
               datetime_metadatas.append(Path.get_datatime_from_exif(metadatas.get('DateTime')))
               datetime_metadatas.append(Path.get_datatime_from_exif(metadatas.get('DateTimeOriginal')))
               # # # The 'DateTimeDigitized' can be a date before than the photo has taken \ weired!
               # datetime_metadatas.append(Path.get_datatime_from_exif(metadatas.get('DateTimeDigitized')))
          except:
               pass
          finally:
               datetime_metadatas_res = [i for i in datetime_metadatas if i != None]
               return datetime_metadatas_res

    def __init__(self, path, USE_EXIFTAGS, USE_FILE_NAME_DATETIME) -> None:
        path_and_file_name, file_extension = os.path.splitext(path)
        if Path.__is_file__(path, file_extension):
            self.is_file = True
            self.file_extension = file_extension.lower()
            self.file_type = IMG if Path.__validate_file_extension_as_photo__(self.file_extension) else DOC
            full_path_list = path_and_file_name.split(PATTERN_SLASH)
            self.file_name = full_path_list.pop(-1)
            self.directory_path = '/'.join(full_path_list)
            self.full_path = f'{self.directory_path}/{self.file_name}{file_extension}'
            if USE_EXIFTAGS and Path.__validate_file_extension_as_image__(file_extension):
               datetime_metadatas = Path.get_metadata_exiftags(self.full_path)
            else:
               datetime_metadatas = Path.get_datetime_metadatas(self.full_path)
            datetime_metadatas.sort()
            self.datetime_oldest = datetime_metadatas[0]
            if USE_FILE_NAME_DATETIME:
               self.datetime_oldest = Path.get_the_file_name_datetime_better_than_metadatas(self.file_name, self.datetime_oldest)
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
        if Path.__validate_file_extension_as_photo__(self.file_extension):
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
        if Path.__validate_file_extension_as_photo__(self.file_extension):
            if self.get_month() <= 9:
                return f'{end_directory}/fotos/{self.get_year_range()}/{self.get_year()}/{self.get_year()}0{self.get_month()}_{self.get_month_in_full()}'
            else:
                return f'{end_directory}/fotos/{self.get_year_range()}/{self.get_year()}/{self.get_year()}{self.get_month()}_{self.get_month_in_full()}'
        else:
            if self.get_month() <= 9:
                return f'{end_directory}/docs/{self.get_year()}/{self.get_year()}0{self.get_month()}_{self.get_month_in_full()}' 
            else:
                return f'{end_directory}/docs/{self.get_year()}/{self.get_year()}{self.get_month()}_{self.get_month_in_full()}' 