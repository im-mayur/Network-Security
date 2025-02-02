'''
This is used to create the logging functionality of project. Separate log folder with with relevant log files 
will be created for trobleshooting,analysis and keeping trach of workflow of project.
'''

import datetime
import os
import logging

# get current datetime
date_time=datetime.datetime.now()

# formatting date objects into readable strings.
log_file=f'{date_time.strftime("%a_%b_%Y_%H_%M_%S")}.log'

# create a folder named 'logs' in current working directory
log_path=os.path.join(os.getcwd(),"logs")
os.makedirs(log_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(log_path,log_file)


logging.basicConfig(filename=LOG_FILE_PATH,
                    format='[%(asctime)s ] %(lineno)d %(name)s %(levelname)s %(message)s',
                    level=logging.DEBUG)

# # Define a global logger instance
# logger = logging.getLogger("networksecurity")
# logger.setLevel(logging.DEBUG)