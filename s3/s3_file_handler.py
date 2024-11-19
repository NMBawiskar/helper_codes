import traceback
import boto3
import os

from boto3 import s3

from settings import *
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

threads = 64

config = ConfigParser()


config.read('config.ini')

print("Using configuration as below:")
print(config.get('s3','aws_region'))
print(config.get('s3','aws_access_key_id'))
print(config.get('s3','aws_secret_access_key'))   

class S3FileHandler:
    def __init__(self):
        self.client =  boto3.client(
            's3',
         
            region_name= config.get('s3','aws_region'),
            aws_access_key_id = config.get('s3','aws_access_key_id'),
            aws_secret_access_key = config.get('s3','aws_secret_access_key'),
   
            
            
            )
        
            
        self.s3 = boto3.resource(
            service_name='s3',
        
            region_name= config.get('s3','aws_region'),
            aws_access_key_id = config.get('s3','aws_access_key_id'),
            aws_secret_access_key = config.get('s3','aws_secret_access_key'),
   
            
        )


    def __download_s3_key(self, key, path, target, bucket):
        try:
            # Calculate relative path
            rel_path = key['Key'][len(path):]
            # Skip paths ending in /
            if not key['Key'].endswith('/'):
                local_file_path = os.path.join(target, rel_path)
                # Make sure directories exist
                local_file_dir = os.path.dirname(local_file_path)
                # assert_dir_exists(local_file_dir)
                if not os.path.exists(local_file_path):
                    self.client.download_file(bucket, key['Key'], local_file_path)
                    print("Downloaded file: ", local_file_path)
                    
                else:
                    print(f"file already exists. Not downloading..",local_file_path)
                    
                return True
        except Exception as e:
            print(f"Error downloading file: {key['Key']}. Error: {str(e)}")
            return False
        return False


    def download_dir(self, bucket, path, target):
        """
        Downloads recursively the given S3 path to the target directory.
        :param client: S3 client to use.
        :param bucket: the name of the bucket to download from
        :param path: The S3 directory to download.
        :param target: the local directory to download the files to.
        """

        # Handle missing / at end of prefix
        if not path.endswith('/'):
            path += '/'

        paginator = self.client.get_paginator('list_objects_v2')
        for result in paginator.paginate(Bucket=bucket, Prefix=path):
            # Download each file individually
            
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = [executor.submit(self.__download_s3_key, key, path, target, bucket) 
                           for key in result['Contents']]

                for future in as_completed(futures):
                    res = future.result()
                    if res:
                        print("Downloaded file: ", path,res)
        
    
    def check_if_file_name_starts_with_given_date(self, s3_key, date_str):
        fileName = s3_key.split('/')[-1]
        if fileName.startswith(date_str):
            return True
        return False
    
    def download_single_date_data_from_s3_folder(self, bucket, path, target:str, date:datetime):

        """
        Downloads recursively the given S3 path to the target directory.
      
        :param bucket: the name of the bucket to download from
        :param path: The S3 directory to download.
        :param target: the local directory to download the files to.
        :param date: the date to check in the file name
        """
        if not path.endswith('/'):
            path += '/'

        date_str = date.strftime('%Y_%m_%d')

        paginator = self.client.get_paginator('list_objects_v2')
        for result in paginator.paginate(Bucket=bucket, Prefix=path):
            s3_keys = result['Contents']
            keys_of_date = [key for key in s3_keys if self.check_if_file_name_starts_with_given_date(key['Key'], date_str)]
            if len(keys_of_date)>0:
                with ThreadPoolExecutor(max_workers=threads) as executor:
                    futures = [executor.submit(self.__download_s3_key, key, path, target, bucket) 
                            for key in result['Contents']]

                    for future in as_completed(futures):
                        res = future.result()
                        if res:
                            print("Downloaded file: ", path,res)
                    



      
    def download_singleFile_from_s3(self, s3FilePath, target_file_path, bucketName):    
        
        try:
            self.s3.Bucket(bucketName).download_file(s3FilePath, target_file_path)           
        except Exception as e:
            print(e)

    def upload_file_to_s3(self, bucket, upload_s3_key, local_file_path):
       
        try:
            self.client.upload_file(local_file_path, Bucket = bucket, Key=upload_s3_key)
            # print('File upload successful.')
            return True
        except:
            print(traceback.format_exc())
            return False

    def move_file_to_other_dir(self, filename, sourcepath, targetPath, bucketName): 
        try:
          
            sourcepath = sourcepath.replace("\\","/")
            targetPath = targetPath.replace("\\","/")
            print("Source path",sourcepath)
            print("targetPath path",targetPath)
            self.s3.Object(bucketName, targetPath).copy_from(CopySource=bucketName+"/"+sourcepath)
            self.s3.Object(bucketName, sourcepath).delete()

            print(f"Moved file {filename} from dir {sourcepath} to {targetPath} ")
            return True
        except Exception as e:
            print(e)
            return False
        
    def list_all_folders_from_bucket(self, bucket, prefix):
        
        result = self.client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
        print(result)
        for o in result.get('CommonPrefixes'):
            print ('sub folder : ', o.get('Prefix'))