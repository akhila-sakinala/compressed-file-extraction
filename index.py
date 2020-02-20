import bz2
import os
import pathlib
import shutil
import tarfile
from itertools import groupby
from operator import itemgetter
from zipfile import ZipFile
import requests
import rarfile
import gzip
from py7zr import unpack_7zarchive
# import patoolib
from pyunpack import Archive

class CompressedFileExtraction():

    def download_url(self):
        '''main function
        compressed file path : /compresses/file/path
        
        ex: ../download-s3-p1/test_list_files.zip
        '''
        file_path = input("zip file path:")
        file_extention = pathlib.Path(file_path).suffixes;
        destination_path = '../download-s3-p1/'+os.path.basename(file_path).split('.')[0]
        if(file_extention[0] == '.zip'):
            self.extract_zip_files(destination_path,file_path)
        elif(file_extention[0] == '.tar'):
            if len(file_extention) > 1:
                file_alg_mode = file_extention[1]
            else:
                file_alg_mode = '.tar'
            self.extract_tar_files(destination_path,file_path,file_alg_mode)
        elif(file_extention[0] in ['.gz', '.gzip']):
            self.extract_gz_files(destination_path,file_path)
        elif(file_extention[0] in ['.bzip2','.bz2']):
            self.extract_bz_files(destination_path,file_path)
        elif(file_extention[0] in ['.7z','.7zip']):
            self.extract_7z_files(destination_path,file_path)
        elif(file_extention[0] in '.rar'):
            self.extract_rar_files(destination_path,file_path)
        else:
            print("Unable to extract files from",file_path)

    def extract_zip_files(self,destination_path,file_path):
        '''zip files extraction'''
        with ZipFile(file_path,'r') as zip_file:
            zip_file.extractall(destination_path)
            self.group_files(destination_path)

    def extract_tar_files(self,destination_path,file_path,file_alg_mode):
        '''tar files extraction'''
        file_alg_mode = 'r:'+file_alg_mode.split('.')[1]
        with tarfile.open(file_path,file_alg_mode) as tar_file:
            tar_file.extractall(destination_path)
            self.group_files(destination_path)

    def extract_gz_files(self,destination_path,file_path):
        '''gz , gzip file extraction'''
        with open(file_path, 'rb') as file_input:
            with gzip.open(destination_path, 'wb') as file_gz:
                shutil.copyfileobj(file_input, file_bz2)

    def extract_bz_files(self,destination_path,file_path):
        '''bz2 and bzip2 file extraction'''
        with open(file_path, 'rb') as file_input:
            with bz2.open(destination_path, 'wb') as file_bz2:
                shutil.copyfileobj(file_input, file_bz2)

    def extract_7z_files(self,destination_path,file_path):
        '''7z file extraction'''
        os.mkdir(destination_path)
        Archive(file_path).extractall(destination_path)
        self.group_files(destination_path)
        # shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
        # shutil.unpack_archive(file_path,destination_path)
        # self.group_files(destination_path)

    def extract_rar_files(self,destination_path,file_path):
        '''rar file extraction'''
        with rarfile.RarFile(file_path,'r') as rar_file:
            rar_file.extractall(destination_path)
            self.group_files(destination_path)

    def group_files(self,destination_path):
        '''group files according to file type'''
        total_files_list = []
        for path, subdirs,files in os.walk(destination_path):
            for name in files:
                each_file_path = os.path.join(path,name)
                file_type = name if len(name.split('.')) > 1 else name+'.additional'
                each_file_dict = {
                    'file':each_file_path,
                    'type':file_type.split('.')[1]
                }
                total_files_list.append(each_file_dict)
        total_files_list = sorted(total_files_list,key=itemgetter('type'))
        for key,group in groupby(total_files_list,key=lambda each_file:each_file['type']):
            self.store_in_dir(key,list(group))

    def store_in_dir(self,file_type,files):
        '''Store files according to the file types'''
        dirName = os.path.abspath(file_type)
        for i in files:
            pathName = i['file']
            if os.path.exists(dirName):
                if os.path.exists(pathName):
                    dirName = dirName+'/'+os.path.abspath(pathName).split('/')[-2]
                    os.mkdir(dirName)
                    shutil.move(pathName,dirName)
                else:
                    shutil.move(pathName,dirName)
            else:
                os.mkdir(dirName)
                shutil.move(pathName,dirName)

# cfe = compressed file extraction
cfe = CompressedFileExtraction()
cfe.download_url()
