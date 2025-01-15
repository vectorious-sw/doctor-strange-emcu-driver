from emcudt.controllers.base import BaseController
from enum import Enum


class ADCChannel(Enum):
    # ADC3 Values
    ASIC_VOLTMETER = 0       # Corresponds to PC2 (ADC3_INP0)
    NTC = 1                  # Corresponds to PC3 (ADC3_INP0)

    # ADC1 Values
    IO_Test = 2              # Corresponds to PA1 (ADC1_INP1)
    VLV_Current_Control = 3  # Corresponds to PA2 (ADC1_INP2)
    VCC_Current_Control = 4  # Corresponds to PA3 (ADC1_INP3)
    Modulator_DAC = 5        # Corresponds to PA4 (ADC1_INP4)
    AM_Detector_A2D = 6      # Corresponds to PA5 (ADC1_INP5)
    Modulation_Sampler_A2D = 7 # Corresponds to PA6 (ADC1_INP6)
    NTC_A2D_Tester = 8       # Corresponds to PA7 (ADC1_INP7)
    PS_Current_A2D = 9       # Corresponds to PC0 (ADC1_INP8)
    Leakage_Current_A2D = 10 # Corresponds to PC1 (ADC1_INP9)

    # Special value
    ADC_ALL = 99


class ADCController(BaseController):
    """
    Controller for managing DAC-related operations via the EMCU.
    """

    def __init__(self, send_command_func, receive_response_func, send_and_receive_func):
        super().__init__(send_command_func, receive_response_func, send_and_receive_func)
        self.MODULE_SYMBOL = bytes([0x04])

    def get_adc(self, channel: ADCChannel) -> None:
        # Construct command: [DAC, Operation, CH, MSB, LSB]
        command = bytes([channel.value])
        length_msb = (len(command) >> 8) & 0xFF
        length_lsb = len(command) & 0xFF
        length = bytes([length_msb, length_lsb])
        return self.send_and_receive(length + self.MODULE_SYMBOL + command)