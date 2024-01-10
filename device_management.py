import pyvisa
from exception_handling_for_visa import io_handling
from abc import ABC, abstractmethod
from device_interface import InterfaceFactory


class AbsManager(ABC):
    """
    abstract class for managing device's interface
    """
    @abstractmethod
    def add_new_device_interface(self):
        ...

    @abstractmethod
    def read_from_device(self):
        ...

    @abstractmethod
    def write_to_device(self):
        ...

    @abstractmethod
    def get_data(self, address: str):
        ...


class DeviceManager(AbsManager):
    """
    Resource managing class, holds all open interfaces and resource managing
    object
    """

    def __init__(self, factory, rm_bknd: str = "@py"):
        """
        Class constructor
        :param factory: Device Interface factory
        :param rm_bknd: location of the backend package,
        by default uses PyVISA-py
        """
        self._devices: dict = {}
        self._rm: pyvisa.ResourceManager = pyvisa.ResourceManager(rm_bknd)
        self._dev_factory: InterfaceFactory = factory

    @io_handling
    def add_new_device_interface(self, address: str):
        """
        Creates new device interface instance and adds it to dictionary
        :param address: url of a certain device
        """
        interface = self._dev_factory.create_interface(
            rm=self._rm, address=address
        )
        self._devices[address] = interface

    @io_handling
    def read_from_device(self, address: str, encoding: str, command: str,
                         chk_sz: int = None):
        """
        Method for sending read command to the device
        :param address: address of the certain device
        :param encoding: encoding current device accepts
        :param command: command to send
        :param chk_sz: chunk size if necessary
        """
        self._devices[address].read(
            encoding=encoding, command=command, chk_sz=chk_sz
        )

    @io_handling
    def write_to_device(self, address: str, encoding: str, msg: str,
                        trmnt: str, dt_type="f", values=None, sep: str = ","):
        """
        Method for sending write command
        :param address: address of the certain device
        :param encoding: encoding current device accepts
        :param msg: message to send
        :param trmnt: termination literal
        :param dt_type: data type literal
        :param values: values required to be sent - if necessary
        :param sep: separator for the values
        """
        self._devices[address].write(
            msg=msg, trmnt=trmnt, encoding=encoding, dt_type=dt_type,
            values=values, sep=sep
        )

    def get_data(self, address: str):
        """
        method for retrieving data, gathered from certain device
        :param address: address of the required device
        :return: List
        """
        return self._devices[address].retrieved_data
