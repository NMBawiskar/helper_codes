import os
import csv
from datetime import datetime, timedelta

proj_dir = os.path.abspath(os.path.dirname(__file__))
csv_file_path = os.path.join(proj_dir, 'dirs_to_clean.csv')

def get_date_str_from_file_name(file_name):
    """file_name format f'{date_}__{time_}.txt'"""
    date_part = file_name.split('.')[0]
    if 'logs_' in date_part:
        date_part = date_part.replace('logs_','')

    date_time = datetime.strptime(date_part, '%Y-%m-%d__%H_%M_%S')
    return date_time


def if_file_name_less_than_given_time(file_name, t:datetime):
    date_time = get_date_str_from_file_name(file_name)
    return date_time < t


def clear_dir(dir_path, days_to_keep):
    files = os.listdir(dir_path)
    timeNow = datetime.now()
    t = timeNow - timedelta(days=days_to_keep)

    files_to_remove = [file for file in files if if_file_name_less_than_given_time(file, t)]
    file_paths_to_remove = [os.path.join(dir_path, file_name) for file_name in files_to_remove]
    for file_path in file_paths_to_remove:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f'Error while removing file {file_path}: {str(e)}')
    print(f'Cleaned directory (prog_name {dir_path}. Removed {len(files_to_remove)} files.')
    


def main():
    with open(csv_file_path, 'r') as f:
        reader = csv.DictReader(f)
    
        
        for dict_item in reader:
            try:
                prog_name, log_dir_path, days_to_keep_logs = dict_item['prog_name'], dict_item['log_dir_path'], int(dict_item['days_to_keep_logs'])
                if os.path.exists(log_dir_path):
                    print(f'Cleaning directory (prog_name {prog_name}) : {log_dir_path} ')
                    clear_dir(log_dir_path, days_to_keep_logs)
                else:
                    print(f'Directory {log_dir_path} does not exist.')
            except Exception as e:
                print(f'Error while processing prog_name {prog_name}: {str(e)}')


if __name__ == '__main__':
        main()