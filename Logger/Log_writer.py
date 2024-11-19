import os
import csv
from datetime import datetime
import time
from dateutil import tz
from typing import List

class LogPrinter:
    LOG_INFO = "INFO"
    LOG_ERROR = "ERROR"
    LOG_OUTPUTS = "OUTPUT"
    LOG_PROCESS_START = "PROCESS_START"
    LOG_PROCESS_END = "PROCESS_END"
    TIME_ZONE_UTC = "UTC"
    TIME_ZONE_IST = "IST"


    def __init__(self, logDirPath, toSaveDataInLogFile =True, toLogWithTimeStamp = True, 
                 logWithFileOrJobName = False, toLogErrorSeperately = True,
                 timeZoneIST=False, delta_min_new_file = 1):
        """Class to write and print logs
        params : logFilePath = filePath (fileType supported any of ('txt' or 'csv')), 
        toLogWithTimeStamp : True (for printing and saving with time stamp)
        timeZoneIST : if False, will store UTC time, elif True, IST time.        
        """

        self.parentLogDirPath = logDirPath

        self.logDirPath = os.path.join(self.parentLogDirPath, 'logs')
        self.error_log_dir = os.path.join(self.parentLogDirPath, "errors")
        self.toSaveDataInLogFile = toSaveDataInLogFile
        self.fileExtention = ""
        self.to_change_time=True
        self.to_change_day_time = True
        
        self.delta_min_new_file=delta_min_new_file
        
        self.writer = None
        self.logWithTimeStamp = toLogWithTimeStamp
        self.logWithFileOrJobName = logWithFileOrJobName

        self.toLogErrorSeperately = toLogErrorSeperately

        if timeZoneIST:
            self.timStampInUST_or_IST = self.TIME_ZONE_IST
        else:
            self.timStampInUST_or_IST = self.TIME_ZONE_UTC


        date_,time_= self.__get_current_date_time()
        time_=time_.replace(':','_')
        hour_str=time_.split('_')[0]
        
        
        self.start_date_time=datetime.now()
        self.fileName=f'{date_}__{time_}.txt'
        self.fileNameError=f'{date_}__{time_}.txt'
        
        self.__create_error_log_dir()

        self.last_logged_date = datetime.today().strftime('%Y-%m-%d')
        

        # os.makedirs(self.logFilePath , exist_ok=True)

    def __create_error_log_dir(self):
        os.makedirs(self.parentLogDirPath, exist_ok=True)
        os.makedirs(self.logDirPath, exist_ok=True)

        if self.toLogErrorSeperately:
            self.error_log_dir = os.path.join(self.logDirPath, "errors")
            os.makedirs(self.error_log_dir, exist_ok=True)



    def __check_file_extension(self):        
        # self.logFileName = os.path.basename(self.fileName)
        self.fileExtention = self.fileName.split(".")[-1]
        if self.fileExtention not in ['txt','csv']:
            return False
        return True

    def __write_data_csv(self, dataList:list):
        '''Function that opens up the file and apppends the content and write the header to it
        Parameter : data -> List of header elements'''

        file_path=os.path.join(self.logDirPath,self.fileName)
        f = open(file_path, 'a+', newline="")
        self.writer = csv.writer(f)        
        self.writer.writerow(dataList)
    
    def __write_data_txt(self, dataString, logType):
        
        file_path=os.path.join(self.logDirPath, self.fileName)
        with open(file_path, 'a+') as f:
            str_to_write = dataString + "\n"
            f.write(str_to_write)

        if self.toLogErrorSeperately:
            if logType == LogPrinter.LOG_ERROR:
                file_path_error = os.path.join(self.error_log_dir, self.fileNameError)
                with open(file_path_error, 'a+') as f:
                    str_to_write = dataString + "\n"
                    f.write(str_to_write)
            
        
    def write_program_logs(self, logType="INFO", logText="", fileUnderProcess="", printOnConsole=True):
        """Write program logs with timestamp or without timestap
        params : logTypes:        
        """
        try:
    
            # for create new file after every day
            current_date_time=datetime.now()
            date_,time_= self.__get_current_date_time()
            time_=time_.replace(':','_')
            hour_str=time_.split('_')[0]

            if self.to_change_day_time: 
                if self.last_logged_date != datetime.today().strftime('%Y-%m-%d'):
                    self.fileName =f'{date_}__00_00_00.txt'
                    self.fileNameError =f'{date_}__00_00_00.txt'

                    self.last_logged_date = datetime.today().strftime('%Y-%m-%d')



            # if hour_str == '00' and self.to_change_day_time == True:
            #     self.fileName =f'{date_}__{time_}.txt'
            #     self.fileNameError =f'{date_}__{time_}.txt'
            #     self.to_change_time=False
            #     self.start_date_time = current_date_time
            #     self.to_change_day_time=False

            # if hour_str > '00':
            #     self.to_change_day_time=True


            list_data = []
            if self.logWithTimeStamp:
                dt_str, time_str = self.__get_current_date_time()
                list_data.append(f"{dt_str}::{time_str}")
            
            list_data.extend([logType, logText])
            
            typeLogStr = f"[{logType}]"
            seperator = " :: "
            string_output = f"{typeLogStr.ljust(10)}"
            if self.logWithTimeStamp:
                string_output+= seperator
                string_output += f"{dt_str}__{time_str}"
            if self.logWithFileOrJobName:
                string_output+= seperator
                string_output += f"{fileUnderProcess.ljust(10)}"
            
            string_output += seperator
            string_output += f"{logText} "


            # if self.logWithTimeStamp:
            #     string_output = f"{typeLogStr.ljust(10)} {dt_str}__{time_str} :: {fileUnderProcess.ljust(10)} ::{logText} "
            # else:
            #     string_output = f"{typeLogStr.ljust(10)} :: {logText}"
            
            if printOnConsole:
                print(string_output)
            
            if self.toSaveDataInLogFile==True:
                if self.__check_file_extension() is not True:
                    print("fileType entered is not supported. Please enter either csv or txt file path only.")
                    return AttributeError
                
                if self.fileExtention =='csv':
                    self.__write_data_csv(dataList=list_data)
                if self.fileExtention=='txt':
                    self.__write_data_txt(dataString=string_output, logType=logType)
        
        except Exception as e:
            print(f"Error occurred while writing logs: {str(e)}")
        

    
    def __get_current_date_time(self):
        
        timeNowUTC = datetime.now()        
        timeNowToParse = timeNowUTC
        
        if self.timStampInUST_or_IST == self.TIME_ZONE_IST:
            timeNowIST = self.__convert_UTC_to_IndiaTime(timeNowUTC)
            timeNowToParse = timeNowIST


        dtStr = timeNowToParse.strftime("%Y-%m-%Y")
        timeStr = timeNowToParse.strftime("%H:%M:%S")

        return [dtStr, timeStr]
    
    
    def __convert_UTC_to_IndiaTime(self, timeUTC:datetime):
        to_zone = tz.gettz('Asia/Kolkata')   
        istTime = timeUTC.astimezone(to_zone)
        return istTime
    



class MultipleLogger:
    def __init__(self, list_loggers:List[LogPrinter]):
        self.loggers = list_loggers
    

    def write_program_logs(self, logType="INFO", logText="", fileUnderProcess="", printOnConsole=True):
        for logger in self.loggers:
            logger.write_program_logs(logType, logText, fileUnderProcess, printOnConsole)