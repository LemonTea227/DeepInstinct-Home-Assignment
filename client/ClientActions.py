from curses.ascii import isdigit
import socket
import tcp_by_size
from MyLogger import MyLogger

IP = '127.0.0.1'
PORT = 22073
logger = MyLogger()


class ClientActions:
    def __init__(self):
        pass

    def connect_client(self):
        """
        Opens a new socket connection to the server
        Initialization is performed for self.client_socket
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((IP, PORT))

    def disconnect_client(self):
        """
        Closes the socket connection to the server
        """
        self.client_socket.close()

    @logger.add_exit_msg(f"returning the result: {is_valid} for the request input: {request}")
    def is_request_valid(self, request: str) -> bool:
        """Check if the request is valid (is included in the available commands)

        Return:
            True if valid, False if not
        """
        logger.info("---- Function valid_request Enter ----")

        lst_request = request.split('~')
        logger.info("Splitted the request to command and parameters")
        request_type = lst_request[0].upper()
        logger.info(
            "Made sure that 'EXIT' command will work even if not written in upper case letters")
        is_valid = False
        logger.info("Starting to check validations")

        if request_type == '+' or request_type == '-' or request_type == '/' or request_type == '*' or request_type == '**' or request_type == '%':
            is_valid = len(lst_request) == 3
            logger.info(
                "Checked if a math operation got the right amount of parameters (operation + 2 parameters)")
        elif request_type == 'EXIT':
            is_valid = len(lst_request) == 1
            logger.info("Checked if the EXIT command got no parameters")

        for number in lst_request[1:]:
            if not isdigit(number):
                is_valid = False
                logger.info("Param: '{number}' is not a number")
                break
        logger.info("Checked if parameters are numbers only")

        logger.info(
            f"---- Function valid_request Exit - returning the result: {is_valid} for the request input: {request} ----")
        return is_valid

    def send_request_to_server(self, request: str) -> None:
        """Send the request to the server. First the length of the request (2 digits), then the request itself"""
        tcp_by_size.send_with_size(self.client_socket, request)

    def print_server_response(self) -> None:
        """Receive the response from the server and printing the response"""
        message = tcp_by_size.recv_by_size(self.client_socket)
        print(message)
