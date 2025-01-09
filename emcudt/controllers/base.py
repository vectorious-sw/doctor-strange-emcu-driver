class BaseController:
    """
    Base class for all EMCU controllers.
    """

    def __init__(self, send_command_func, receive_response_func, send_and_receive_func):
        """
        Initialize the base controller.

        Args:
            send_command_func (callable): Function to send a command to the EMCU.
            receive_response_func (callable): Function to receive a response from the EMCU.
            send_and_receive_func (callable): Function to send a command and wait for the response.
        """
        self._send_command = send_command_func
        self._receive_response = receive_response_func
        self._send_and_receive = send_and_receive_func

    def send_command(self, command: bytes) -> None:
        """
        Send a command to the EMCU (default implementation).
        """
        self._send_command(command)

    def receive_response(self) -> bytes:
        """
        Receive a response from the EMCU (default implementation).
        """
        return self._receive_response()

    def send_and_receive(self, command: bytes) -> bytes:
        """
        Send a command and wait for the response (default implementation).
        """
        return self._send_and_receive(command)
