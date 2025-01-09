from emcudt.driver import EmcuDebuggingTool
from emcudt.controllers.dac import DAC,DacOperation,DacChannel
from emcudt.controllers.gpio import GPIO_NAME,PinState

def main():
    # Initialize driver
    emcu = EmcuDebuggingTool(port="/dev/tty.usbmodem3447336B30331")
    try:
        emcu.connect()
        # emcu.dac.debug_send_and_receive(DAC.DAC2, DacChannel.CH1, 2.2)
        emcu.gpio.GPIO_Control(GPIO_NAME.C_EXT_CTRL0,PinState.GPIO_PIN_SET)
    finally:
        emcu.disconnect()

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    main()
