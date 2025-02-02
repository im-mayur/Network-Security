import datetime
import os
import logging

x=datetime.datetime.now()
print(x.strftime("%a_%b_%Y_%H_%M_%S"))
log_file=f'{x.strftime("%a_%b_%Y_%H_%M_%S")}.log'
print(log_file)

