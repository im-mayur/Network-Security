import sys
from networksecurity.logging import logger



class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()

        self.line_no=exc_tb.tb_lineno
        self.filename=exc_tb.tb_frame.f_code.co_filename

        logger.logging.error(f"Error occurred in python script name [{self.filename}] at line number [{self.line_no}] error message [{self.error_message}]")


    ## The __str__() function controls what should be returned when the class object is represented as a string.
    def __str__(self):
         return ("Error occured in python script name [{0} at line number [{1}] error message [{2}]]".format(
            self.filename,self.line_no,str(self.error_message)
        ))
    

    
if __name__=='__main__':
    try:
        logger.logging.info("entered the try block")
        a=1/0

    except Exception as e:
        raise NetworkSecurityException(e,sys)
        