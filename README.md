# This is my implementation of class for managing connection to remote scientific devices

## Description:
This task required creation of class with following functionality:
-establish connection to remote device
-send read and write commands
-store retrieved data for following processing

### Additional notes:
To use, you need to instantiate DeviceManager class,
to make this you need to pass an AbstractInterface class
After that you can add instances of different devices to DeviceManager
To execute read, write operations and get data - use appropriate methods 

## Requirements:
# Python:
- [Python 3.11](https://www.python.org/downloads/)
# Significant Libraries and Frameworks:
-[PyVISA 1.14.1](https://pyvisa.readthedocs.io/en/stable/)
-[PyVISA-py 0.7.1](https://pyvisa.readthedocs.io/projects/pyvisa-py/en/latest/)