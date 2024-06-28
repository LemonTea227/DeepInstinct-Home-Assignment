from curses.ascii import isdigit
import socket
import tcp_by_size
from my_logger import MyLogger

IP = "127.0.0.1"
PORT = 22073
logger = MyLogger()


class ClientActions:
    def __init__(self):
        pass

    @logger.log_function
    def connect_client(self):
        """
        Opens a new socket connection to the server
        Initialization is performed for self.client_socket
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((IP, PORT))

    @logger.log_function
    def disconnect_client(self):
        """
        Closes the socket connection to the server
        """
        self.client_socket.close()

    @logger.log_function
    def validate_request(self, request: str) -> bool:
        """
        Check if the request is valid (is included in the available commands)

        :param request: _description_
        :return: True if valid, False if not
        """
        lst_request: list[str] = request.split("~")
        logger.info("Splitted the request to command and parameters")
        lst_request[0] = lst_request[0].upper()
        logger.info(
            "Made sure that 'EXIT' command will work even if not written in upper case letters"
        )
        logger.info("Starting to check validations now")
        is_valid = self.validate_math_operation(lst_request)
        logger.info("validated if the request is valid math operation")

        if not is_valid:
            is_valid = self.validate_exit_operation(lst_request)

        logger.info(
            f"returning the result: {is_valid} for the request input: {request}"
        )
        return is_valid

    @logger.log_function
    def validate_math_operation(self, lst_request: list[str]) -> bool:
        """
        validate that the operation is a valid math operation

        :param lst_request: splitted request to fields
        :return: if the operation is a valid math operation
        """
        is_valid: bool = False
        request_type = lst_request[0]
        if request_type in ("+", "-", "/", "*", "**", "%"):
            is_valid = len(lst_request) == 3
            logger.info(
                "Checked if a math operation got the right amount of"
                " parameters (operation + 2 parameters)"
            )

            for number in lst_request[1:]:
                if not isdigit(number):
                    is_valid = False
                    logger.info("Param: '{number}' is not a number")
                    break
                logger.info("Checked if parameters are numbers only")

        return is_valid

    @logger.log_function
    def validate_exit_operation(self, lst_request: list[str]) -> bool:
        """
        validate that the operation is a valid exit operation

        :param lst_request: splitted request to fields
        :return: if the operation is a valid exit operation
        """
        request_type = lst_request[0]
        return request_type == "EXIT" and len(lst_request) == 1

    @logger.log_function
    def send_request_to_server(self, request: str) -> None:
        """
        Send the request to the server. First the length of the request
         (2 digits), then the request itself
        """
        tcp_by_size.send_with_size(self.client_socket, request)

    @logger.log_function
    def print_server_response(self) -> None:
        """
        Receive the response from the server and printing the response
        """
        message = tcp_by_size.recv_by_size(self.client_socket).decode()
        print(message)
