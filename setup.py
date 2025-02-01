'''
In Python, setup.py is a module used to build and distribute Python packages. It typically contains information about 
the package, such as its name, version, and dependencies, as well as instructions for building and installing the package.
This information is used by the pip tool, which is a package manager for Python that allows users to install and manage 
Python packages from the command line. By running the setup.py file with the pip tool, you can build and distribute your
Python package so that others can use it.
'''


from setuptools import setup,find_packages
from typing import List

def get_requirements()->List[str]:
    '''
    This function returns the list of requirements to be installed for dependancies in projects.

    Must have file named "requirements.txt" with all the dependancies in your project structure,
    as dependancies will be read from that file.
    '''

    try:
        requirement_list=[]
        # open the file in read mode
        with open('requirements.txt', 'r') as file:  
            lines=file.readlines()

            # read each line and remove spaces
            for line in lines:
                requirement=line.strip()
                if requirement and requirement!='-e .':
                    requirement_list.append(requirement)
        
    except FileNotFoundError:
        print(' file named requirements.txt not found')

    return requirement_list



## setup the metadata using setuptools. ##

setup(
    name='Network Security', 
    version='0.0.0.1', 
    description='This is an end to end ml project for network security', 
    author='Mayur Kulkarni', 
    author_email='mayurkulkarni5113@gmail.com', 
    packages=find_packages(), 
    install_requires=get_requirements()
)