import serial
import time
from .logging_config import setup_logger
from emcudt.utils import append_crc32
from emcudt.controllers.dac import DACController
from emcudt.controllers.gpio import GPIOController
from emcudt.controllers.adc import ADCController

# Initialize the logger
logger = setup_logger()


class EmcuDebuggingTool:
    """
    Python driver for communicating with the Doctor Strange system via the EMCU.
    """

    def __init__(self, port, baudrate=9600, timeout=1):
        """
        Initialize the driver.

        Args:
            port (str): The COM port to connect to (e.g., "/dev/ttyUSB0").
            baudrate (int): Communication speed (default: 9600).
            timeout (float): Timeout for serial communication (default: 1 second).
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None
        self.HEADER = bytes([0x56, 0x45])  # Header bytes for 'V' and 'E'

        # Initialize controllers
        self.dac = DACController(send_command_func=self._send_command, receive_response_func=self._receive_response, send_and_receive_func=self._send_and_receive)
        self.gpio = GPIOController(send_command_func=self._send_command, receive_response_func=self._receive_response, send_and_receive_func=self._send_and_receive)
        self.adc = ADCController(send_command_func=self._send_command, receive_response_func=self._receive_response,send_and_receive_func=self._send_and_receive)

    def _add_header(self, data: bytes) -> bytes:
        """
        Adds a header of 'V' (0x56) and 'E' (0x45) to the start of a byte array.

        Args:
            data (bytes): The original byte array.

        Returns:
            bytes: A new byte array with the header prepended.
        """
        return self.HEADER + data

    def connect(self):
        """Establish a connection to the EMCU."""
        try:
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
            )
            logger.info(f"Connected to EMCU on {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            logger.error(f"Failed to connect: {e}")
            self.connection = None

    def disconnect(self):
        """Close the connection to the EMCU."""
        if self.connection and self.connection.is_open:
            self.connection.close()
            logger.info("Disconnected from EMCU.")

    def _send_raw_command(self, command : bytes):
        """
        Send a command to the EMCU.

        Args:
            command (bytes): The command to send, as a byte array.
        """
        if not self.connection or not self.connection.is_open:
            logger.error("Attempted to send command without a connection.")
            raise ConnectionError("Not connected to EMCU.")

        self.connection.write(command)
        logger.debug(f"Sent: {command.hex()}")

    def _send_command(self, command: bytes):
        """
        Send a command to the EMCU.

        Args:
            command (bytes): The command to send, as a byte array.
        """
        if not self.connection or not self.connection.is_open:
            logger.error("Attempted to send command without a connection.")
            raise ConnectionError("Not connected to EMCU.")

        self.connection.write(append_crc32(self._add_header(command)))
        logger.debug(f"Sent: {command.hex()}")

    def _receive_response(self):
        """
        Receive a response from the EMCU.

        Returns:
            bytes: The response received from the EMCU.
        """
        if not self.connection or not self.connection.is_open:
            logger.error("Attempted to receive response without a connection.")
            raise ConnectionError("Not connected to EMCU.")

        response = self.connection.read_until(b'\n')  # Adjust terminator as per protocol
        logger.debug(f"Received: {response.hex()}")
        return response

    def _send_and_receive(self, command):
        """
        Send a command and wait for the response.

        Args:
            command (bytes): The command to send, as a byte array.

        Returns:
            bytes: The response received from the EMCU.
        """
        self.connection.write(append_crc32(self._add_header(command)))
        time.sleep(0.5)  # Wait for response (adjust based on system timing)
        return self._receive_response()

    def is_connected(self):
        """Check if the driver is connected."""
        connected = self.connection and self.connection.is_open
        logger.info(f"Connection status: {'Connected' if connected else 'Not Connected'}")
        return connected
