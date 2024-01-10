from abc import ABC, abstractmethod
import pyvisa
from typing import Literal
from pyvisa.resources import MessageBasedResource


class InterfaceAbsFactory(ABC):
    """
    Abstract factory for creation of Device Interface object
    """
    @staticmethod
    @abstractmethod
    def create_interface(rm: pyvisa.ResourceManager, address: str):
        ...


class InterfaceFactory(InterfaceAbsFactory):
    """
    Actual implementation of Device Interface object
    """
    @staticmethod
    def create_interface(rm: pyvisa.ResourceManager, address: str):
        return DeviceInterface(rm=rm, address=address)


class AbstractInterface(ABC):
    """
    Abstract implementation of Device Interface
    """
    @abstractmethod
    def read(self, encoding: str, command: str, chk_sz: int = None):
        ...

    @abstractmethod
    def write(self, msg: str, trmnt: str, encoding: str, is_b_end: bool,
              dt_type: Literal['s', 'b', 'c', 'd', 'o', 'x', 'X', 'e', 'E', 'f', 'F', 'g', 'G'],
              values=None, sep: str = ","):
        ...


class DeviceInterface(AbstractInterface):
    """
    Current implementation of Device Interface class
    """
    def __init__(self, rm, address: str):
        """
        Class constructor
        :param rm: pyvisa.ResourceManager instance
        :param address: tcpip socket formatted address
        """
        self.retrieved_data = []
        self._inst: MessageBasedResource = rm.open_resource(address)

    def read(self, encoding: str, command: str, chk_sz: int = None):
        data = None
        if chk_sz:
            self._inst.chunk_size = chk_sz
        if encoding == "ascii":
            data = self._inst.query(command)
        elif encoding == "bytes":
            data = self._inst.read_binary_values()
        self.retrieved_data.append(data)

    def write(self, msg: str, trmnt: str, encoding: str, is_b_end: bool,
              dt_type: Literal['s', 'b', 'c', 'd', 'o', 'x', 'X', 'e', 'E',
              'f', 'F', 'g', 'G'],
              values=None, sep: str = ","):
        if not values:
            self._inst.write(msg)
        elif encoding == "ascii":
            self._inst.write_ascii_values(message=msg, values=values,
                                          separator=sep, termination=trmnt)
        elif encoding == "bytes":
            self._inst.write_binary_values(message=msg, values=values,
                                           datatype=dt_type,
                                           is_big_endian=is_b_end,
                                           termination=trmnt)
