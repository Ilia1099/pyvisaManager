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
