import time
from req_classes.s3_file_handler import S3FileHandler
from configparser import ConfigParser
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback
from datetime import datetime


config = ConfigParser()

config.read('config.ini')
list_dirs = [r'data_collection/right/imgs', r'data_collection/right/annotations',
             r'data_collection/left/imgs', r'data_collection/left/annotations']

list_dirs = [r'data_annotated/right/imgs', r'data_annotated/right/annotations',
             r'data_annotated/left/imgs', r'data_annotated/left/annotations']


bucket= config.get('s3','bucket_name')
n_batch = 16


s3FileHandler = S3FileHandler()
s3FileHandler.list_all_folders_from_bucket(bucket, prefix="")
# single_date_to_data_to_download = datetime(2024,11,11)
for dir in list_dirs:
    os.makedirs(dir, exist_ok=True)
    try:
        s3FileHandler.download_dir(bucket, dir, dir)
    except Exception as e:
        print(f"Error in downloading {dir}: {traceback.format_exc()}")
    # s3FileHandler.download_single_date_data_from_s3_folder(bucket, dir, dir, single_date_to_data_to_download )
    