
from emcudt.controllers.base import BaseController
from enum import Enum

class PotentiometerOperation(Enum):
    """
    Enum to represent DAC operations.
    """
    SET = 0x00

class PotentiometerController(BaseController):
    """
    Controller for managing DAC-related operations via the EMCU.
    """

    def __init__(self, send_command_func, receive_response_func, send_and_receive_func):
        super().__init__(send_command_func, receive_response_func, send_and_receive_func)
        self.MODULE_SYMBOL = bytes([0x03])

    def set_wiper_register(self,resistance) -> None:
        """
        Set the wiper register of the MCP401x.

        Args:
            :param resistance: MAX value is 0x7F  =  127

        """
        if resistance > 127 or resistance< 0 :
            raise Exception("max resistence is 127")
        # Construct command: [DAC, Operation, CH, MSB, LSB]
        command = bytes([PotentiometerOperation.SET.value,resistance])
        length_msb = (len(command) >> 8) & 0xFF
        length_lsb = len(command) & 0xFF
        length = bytes([length_msb, length_lsb])
        self.send_command(length + self.MODULE_SYMBOL + command)