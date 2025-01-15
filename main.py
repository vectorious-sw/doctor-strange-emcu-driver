from emcudt.driver import EmcuDebuggingTool
from emcudt.controllers.dac import DAC,DacOperation,DacChannel
from emcudt.controllers.gpio import GPIO_NAME,PinState
from emcudt.controllers.adc import ADCChannel

def main():
    # Initialize driver
    emcu = EmcuDebuggingTool(port="/dev/tty.usbmodem3447336B30331")
    try:
        emcu.connect()
        ntc = emcu.adc.get_adc(ADCChannel.ADC_ALL)
        # emcu.gpio.GPIO_Control(GPIO_NAME.VCO_EN,PinState.GPIO_PIN_RESET)
    finally:
        emcu.disconnect()

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    main()
