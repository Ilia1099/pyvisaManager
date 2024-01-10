import pyvisa
from typing import Literal
from pyvisa.resources import MessageBasedResource
from pyvisa.errors import VisaIOError
import logging

logger = logging
logger.basicConfig(level=logging.ERROR)


def io_handling(func):
    """
    decorator for handling "VisaIOError" exception which happens in case of
    connection issues
    """
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except VisaIOError as e:
            logger.error(
                f"Exception, device: {kwargs['device_url']}",
                exc_info=True)
    return wrapper


class InterfaceFactory:
    """
    Device Interface class factory
    """
    @staticmethod
    def create_interface(rm: pyvisa.ResourceManager, address: str):
        return DeviceInterface(rm=rm, address=address)


class DeviceInterface:
    """
    Device Interface class
    """
    def __init__(self, rm: pyvisa.ResourceManager, address: str):
        """
        Class constructor
        :param rm: pyvisa.ResourceManager instance
        :param address: tcpip socket formatted address
        """
        self.retrieved_data = []
        # noinspection PyTypeChecker
        self._inst: MessageBasedResource = rm.open_resource(address)

    @io_handling
    def read(self, encoding: str, command: str, chk_sz: int = None):
        data = None
        if chk_sz:
            self._inst.chunk_size = chk_sz
        if encoding == "ascii":
            data = self._inst.query(command)
        elif encoding == "bytes":
            data = self._inst.read_binary_values()
        self.retrieved_data.append(data)

    @io_handling
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

