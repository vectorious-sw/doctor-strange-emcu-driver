
from emcudt.controllers.base import BaseController
from enum import Enum


class DAC(Enum):
    DAC1 = 1
    DAC2 = 2


class DacOperation(Enum):
    """
    Enum to represent DAC operations.
    """
    LOAD_AND_POWER_UP = 0x00
    LOAD = 0x01
    ON = 0x02
    OFF = 0x03


class DacChannel(Enum):
    """
    Enum to represent DAC channels.
    """
    CH1 = 0
    CH2 = 1
    CH3 = 2
    CH4 = 3
    ALL = 15


class DACController(BaseController):
    """
    Controller for managing DAC-related operations via the EMCU.
    """

    def __init__(self, send_command_func, receive_response_func, send_and_receive_func):
        super().__init__(send_command_func, receive_response_func, send_and_receive_func)
        self.MODULE_SYMBOL = bytes([0x00])

    def set_voltage(self, dac: DAC, channel : DacChannel, voltage: float) -> None:
        """
        Set the output voltage of a specified DAC.

        Args:
            dac (int): The DAC (1 or 2).
            channel (int) : the Dac Channel
            voltage (float): The desired voltage.

        """
        voltage_int = int(voltage * 1000)  # Assume voltage resolution of 0.01V
        voltage_msb = (voltage_int >> 8) & 0xFF
        voltage_lsb = voltage_int & 0xFF

        # Construct command: [DAC, Operation, CH, MSB, LSB]
        command = bytes([dac.value, DacOperation.LOAD.value, channel.value, voltage_msb, voltage_lsb])
        length_msb = (len(command) >> 8) & 0xFF
        length_lsb = len(command) & 0xFF
        length = bytes([length_msb, length_lsb])
        self.send_command(length + self.MODULE_SYMBOL + command)

    def set_voltage_and_power_up(self, dac: DAC, channel : DacChannel, voltage: float) -> None:
        """
        Power up the specified DAC.

        Args:
            dac_id (int): The ID of the DAC (1 or 2).
        """
        voltage_int = int(voltage * 1000)  # Assume voltage resolution of 0.01V
        voltage_msb = (voltage_int >> 8) & 0xFF
        voltage_lsb = voltage_int & 0xFF

        # Construct command: [DAC, Operation, CH, MSB, LSB]
        command = bytes([dac.value, DacOperation.LOAD_AND_POWER_UP.value, channel.value, voltage_msb, voltage_lsb])
        length_msb = (len(command) >> 8) & 0xFF
        length_lsb = len(command) & 0xFF
        length = bytes([length_msb,length_lsb])
        self.send_command(length + self.MODULE_SYMBOL + command)

    def power_up(self,  dac: DAC, channel : DacChannel) -> None:
        """
        Power up the specified DAC.

        Args:
            dac_id (int): The ID of the DAC (1 or 2).
        """

        # Construct command: [DAC, Operation, CH, MSB, LSB]
        command = bytes([dac.value, DacOperation.ON.value, channel.value, 0, 0])
        length_msb = (len(command) >> 8) & 0xFF
        length_lsb = len(command) & 0xFF
        length = bytes([length_msb, length_lsb])
        self.send_command(length + self.MODULE_SYMBOL + command)

    def power_down(self,  dac: DAC, channel : DacChannel) -> None:
        """
        Power down the specified DAC.

        Args:
            dac_id (int): The ID of the DAC (1 or 2).
        """

        # Construct command: [DAC, Operation, CH, MSB, LSB]
        command = bytes([dac.value, DacOperation.OFF.value, channel.value, 0, 0])
        length_msb = (len(command) >> 8) & 0xFF
        length_lsb = len(command) & 0xFF
        length = bytes([length_msb, length_lsb])
        self.send_command(length + self.MODULE_SYMBOL + command)

    def debug_send_and_receive(self, dac: DAC, channel : DacChannel, voltage: float) -> None:
        """
        Power up the specified DAC.

        Args:
            dac_id (int): The ID of the DAC (1 or 2).
        """
        voltage_int = int(voltage * 1000)  # Assume voltage resolution of 0.01V
        voltage_msb = (voltage_int >> 8) & 0xFF
        voltage_lsb = voltage_int & 0xFF

        # Construct command: [DAC, Operation, CH, MSB, LSB]
        command = bytes([dac.value, DacOperation.LOAD_AND_POWER_UP.value, channel.value, voltage_msb, voltage_lsb])
        length_msb = (len(command) >> 8) & 0xFF
        length_lsb = len(command) & 0xFF
        length = bytes([length_msb,length_lsb])
        self._send_and_receive(length + self.MODULE_SYMBOL + command)



