from dataclasses import dataclass



'''
The dataclass provides an in built __init__() constructor to classes which handle the dat
a and object creation for them. 
'''

@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str