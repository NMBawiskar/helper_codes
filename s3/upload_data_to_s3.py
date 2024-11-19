import time
from req_classes.s3_file_handler import S3FileHandler
from configparser import ConfigParser
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback
from settings import ProjSettings

config = ConfigParser()

config.read('config.ini')

logs = ProjSettings.logs_data_collection

s3FileHandler = S3FileHandler()

bucket= config.get('s3','bucket_name')
n_batch = 16
list_dirs = [r'data_collection/right/imgs', r'data_collection/right/annotations',
             r'data_collection/left/imgs', r'data_collection/left/annotations']

def upload_single_file(path_file):
    try:
        path_file = path_file.replace("\\", '/')
        splits = path_file.split("/")
        # print(splits)
        fileName = os.path.basename(path_file)
        parent_dir, side, sub_dir = splits[-4], splits[-3], splits[-2]
        upload_s3_key = f"{parent_dir}/{side}/{sub_dir}/{fileName}"    

        isUploaded = s3FileHandler.upload_file_to_s3(bucket, upload_s3_key, path_file)
        if isUploaded:
            print(f"File {path_file} uploaded to S3")
            os.remove(path_file)
        else:
            logs.write_program_logs("ERROR", logText=f"Failed to upload file {path_file} to S3")
    except Exception as e:
        logs.write_program_logs("ERROR", logText=f"Error occurred while uploading file: {traceback.format_exc()}")

def upload_data_to_s3():
    count_files_uploaded = 0

    while True:
        for directory in list_dirs:
            print(f"Uploading from directory {directory}")
            files = os.listdir(directory)
            files_batch = files[:n_batch]
            file_paths = [os.path.join(directory, fileName) for fileName in files_batch]
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [executor.submit(upload_single_file, file_path) for file_path in file_paths]

                for future in as_completed(futures):
                    res = future.result()
                    if res:
                        count_files_uploaded += 1
                        # print(f"Successfully uploaded {count_files_uploaded} files")
            
            logs.write_program_logs(logText=f"Uploaded files count : {count_files_uploaded}")
        time.sleep(10)

       


if __name__ == '__main__':
    upload_data_to_s3()