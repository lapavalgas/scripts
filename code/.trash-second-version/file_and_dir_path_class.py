import os
import datetime
import pathlib
from dateutil import parser
from PIL import Image 
from PIL.ExifTags import TAGS 

PATTERN_SLASH = '/'
PATTERN_DOT = '.'

METADATA_NOT_IMAGE_KEY = 'is_image_file'

DATE_TIME = 'DateTime'
DATE_TIME_ORIGINAL = 'DateTimeOriginal'
# DATE_TIME_DIGITIZED = 'DateTimeDigitized'

EXCEPTION_PATH_NONE = 'O script falhou ao ler a path.'

class Path:
    
    directory_path = None
    full_path = None
    is_file = None
    file_name = None
    file_extension = None
    metadata = None
    metadata_oldest_datetime = None

    @classmethod
    def __help_metadata__(cls):
         print(TAGS) 

    def __validate_file_extension__(self):
        if self.file_extension == None:
            return False
        return self.file_extension.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))
    
    @classmethod
    def __is_file__(self, path, file_extension):
        return os.path.isfile(path) or file_extension.__contains__(PATTERN_DOT)
    
    def __generate_failed_to_read_metadata__(self, is_image):
            file_date_time = datetime.datetime.fromtimestamp(os.path.getctime(self.full_path))
            file_date_time_modification = datetime.datetime.fromtimestamp(os.path.getmtime(self.full_path))
            file_date_time_modification_alternative = datetime.datetime.fromtimestamp(pathlib.Path(self.full_path).stat().st_mtime)
            self.metadata_oldest_datetime = file_date_time
            self.metadata = { 
                METADATA_NOT_IMAGE_KEY: is_image,
                DATE_TIME: file_date_time,
                # DATE_TIME_DIGITIZED: file_date_time_modification,
                DATE_TIME_ORIGINAL: file_date_time_modification_alternative
            }
         
    def __generate_image_metadata__(self):
        file_metadatas = {}
        try:
            image = Image.open(self.full_path)
            for tag, value in image._getexif().items():
                if tag in TAGS:
                        file_metadatas[TAGS[tag]] = value
                    # print([TAGS[tag]], value)
            if file_metadatas.get('GPSInfo'):
                file_metadatas.pop('GPSInfo')
            if file_metadatas.get('ComponentsConfiguration'):
                file_metadatas.pop('ComponentsConfiguration')
            if file_metadatas.get('MakerNote'):
                file_metadatas.pop('MakerNote')
            self.metadata = file_metadatas
            if self.metadata.get(DATE_TIME) == None:
                 self.metadata[DATE_TIME] = datetime.datetime.fromtimestamp(os.path.getctime(self.full_path))
            if type(self.metadata.get(DATE_TIME) is str):
                 self.metadata[DATE_TIME] = datetime.datetime.strptime(self.metadata[DATE_TIME], '%Y:%m:%d %H:%M:%S')
            if self.metadata.get(DATE_TIME_ORIGINAL) == None:
                 self.metadata[DATE_TIME_ORIGINAL] = datetime.datetime.fromtimestamp(os.path.getmtime(self.full_path))
            if type(self.metadata.get(DATE_TIME_ORIGINAL) is str):
                 self.metadata[DATE_TIME_ORIGINAL] = datetime.datetime.strptime(self.metadata[DATE_TIME_ORIGINAL], '%Y:%m:%d %H:%M:%S')
            # if self.metadata.get(DATE_TIME_DIGITIZED) == None:
            #      self.metadata[DATE_TIME_DIGITIZED] = datetime.datetime.fromtimestamp(pathlib.Path(self.full_path).stat().st_mtime)
            # if type(self.metadata.get(DATE_TIME_DIGITIZED) is str):
            #      self.metadata[DATE_TIME_DIGITIZED] = datetime.datetime.strptime(self.metadata[DATE_TIME_DIGITIZED], '%Y:%m:%d %H:%M:%S')
        except:
            self.__generate_failed_to_read_metadata__(is_image=True)

    def __init__(self, path) -> None:
        path_and_file_name, file_extension = os.path.splitext(path)
        if Path.__is_file__(path, file_extension) == False:
            self.is_file = False
            self.directory_path = path
            self.full_path = path
        else:
            self.is_file = True
            self.__set_file__(path_and_file_name, file_extension)

    def __set_file__(self, path_and_file_name, file_extension):
        self.file_extension = file_extension
        full_path_list = path_and_file_name.split(PATTERN_SLASH)
        self.file_name = full_path_list.pop(-1)
        self.directory_path = '/'.join(full_path_list)
        self.full_path = f'{self.directory_path}/{self.file_name}{file_extension}'
        if self.__validate_file_extension__():
            self.__generate_image_metadata__()
            self.__get_oldest_date_time__()
        else:  
            self.__generate_failed_to_read_metadata__(is_image=False)
            self.__get_oldest_date_time__()

    def __get_oldest_date_time__(self):
        dates = [
            self.metadata.get(DATE_TIME), 
            self.metadata.get(DATE_TIME_ORIGINAL), 
            # self.metadata.get(DATE_TIME_DIGITIZED)
            ]
        dates_res = [i for i in dates if i != None]
        # dates_less_none = [i for i in dates if i != None]
        # dates_res = []
        # for dt in dates_less_none:
        #      if not type(dt) is datetime.datetime:
        #           dates_res.append(datetime.datetime.strptime(dt, '%Y:%m:%d %H:%M:%S'))
        if dates_res:
            dates_res.sort()
            if type(dates_res[0]) == str:
                 self.metadata_oldest_datetime = datetime.datetime.strptime(dates_res[0], "%Y:%m:%d %H:%M:%S")
            else:
                 self.metadata_oldest_datetime = dates_res[0]
        else:
            self.metadata_oldest_datetime = datetime.datetime.fromtimestamp(os.path.getmtime(self.full_path))
    
    def get_year(self):
         return self.metadata_oldest_datetime.year
    
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
         return self.metadata_oldest_datetime.month
    
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

    def know_the_way(self, end_directory):
        if self.__validate_file_extension__():
            if self.get_month() <= 9: 
                return f'{end_directory}/fotos/{self.get_year_range()}/{self.get_year()}/{self.get_year()}0{self.get_month()}_{self.get_month_in_full()}/{self.file_name}{self.file_extension}'
            else:
                return f'{end_directory}/fotos/{self.get_year_range()}/{self.get_year()}/{self.get_year()}0{self.get_month()}_{self.get_month_in_full()}/{self.file_name}{self.file_extension}'
        else:
            if self.get_month() <= 9:
                return f'{end_directory}/docs/{self.get_year()}/{self.get_year()}0{self.get_month()}_{self.get_month_in_full()}/{self.file_name}{self.file_extension}' 
            else:
                return f'{end_directory}/docs/{self.get_year()}/{self.get_year()}{self.get_month()}_{self.get_month_in_full()}/{self.file_name}{self.file_extension}'

    def know_the_way_directory_path(self, end_directory):
        if self.__validate_file_extension__():
            if self.get_month() <= 9:
                return f'{end_directory}/fotos/{self.get_year_range()}/{self.get_year()}/{self.get_year()}0{self.get_month()}_{self.get_month_in_full()}'
            else:
                return f'{end_directory}/fotos/{self.get_year_range()}/{self.get_year()}/{self.get_year()}0{self.get_month()}_{self.get_month_in_full()}'
        else:
            if self.get_month() <= 9:
                return f'{end_directory}/docs/{self.get_year()}/{self.get_year()}0{self.get_month()}_{self.get_month_in_full()}' 
            else:
                return f'{end_directory}/docs/{self.get_year()}/{self.get_year()}{self.get_month()}_{self.get_month_in_full()}' 

