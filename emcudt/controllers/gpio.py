
from emcudt.controllers.base import BaseController
from enum import Enum

class GPIO_NAME(Enum):
    VCO_EN = 0
    MHZ678_EN = 1
    RESONATOR_INPUT_EN = 2
    V_BURN_VLV_2_2_EN = 3
    V_BURN_VLV_2_5_EN = 4
    V_BURN_OTP_EN = 5
    ASIC_VCC_1_8_EN = 6
    Floating_VCC_EN = 7
    Floating_GND_EN = 8
    PCAP04_MODE = 9
    V_BURN_VLV_2_5_EN_ALT = 10
    ASIC_VLV_1_8_EN = 11
    C_EXT_CTRL0 = 12
    C_EXT_CTRL1 = 13
    C_EXT_CTRL2 = 14
    C_EXT_CTRL3 = 15
    C_EXT_CTRL4 = 16
    VCO_BUFFER_EN = 17

class PinState(Enum):
    GPIO_PIN_RESET = 0
    GPIO_PIN_SET = 1

class GPIOController(BaseController):
    """
    Controller for managing DAC-related operations via the EMCU.
    """

    def __init__(self, send_command_func, receive_response_func, send_and_receive_func):
        super().__init__(send_command_func, receive_response_func, send_and_receive_func)
        self.MODULE_SYMBOL = bytes([0x01])

    def GPIO_Control(self, gpio: GPIO_NAME, state: PinState) -> None:
        """
        Set the output voltage of a specified DAC.

        Args:
            gpio (int): The GPIO name
            state (int) : the target state

        """
        # Construct command: [read/write,GPIO,if write SET/RESET if read unused]
        command = bytes([1,gpio.value, state.value])
        length_msb = (len(command) >> 8) & 0xFF
        length_lsb = len(command) & 0xFF
        length = bytes([length_msb, length_lsb])
        self.send_command(length + self.MODULE_SYMBOL + command)

