from curses.ascii import isdigit
import socket
import tcp_by_size
from typing import Union
import MathOperation
from MyLogger import MyLogger


IP = '0.0.0.0'
PORT = 22073


class ServerActions:
    def __init__(self):
        self.server_socket: socket.socket = None  # type: ignore
        self.client_socket: socket.socket = None  # type: ignore
        self.address: socket._RetAddress = None  # type: ignore
        self.logger = MyLogger()

    def connect_server(self):
        """
        Opens a new socket connection to the client
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen(1)
        self.client_socket, self.address = self.server_socket.accept()

    def disconnect_server(self):
        """
        Closes the socket connection to the client
        """
        self.client_socket.close()
        self.server_socket.close()

    def create_successful_message(self, operation_name: str, params: list[str], answer: str):
        message = f"{operation_name} of {params[0]} and {params[1]} result is: \n{answer}"
        return message

    def create_unsuccessful_message(self, operation_name: str, error_message: str = "") -> str:
        message = f"{operation_name} didn't work: \n{error_message}"
        return message

    def receive_client_request(self) -> Union[bytes, str]:
        """Receives the full message sent by the client

        Works with the protocol defined in the client's "send_request_to_server" function

        Returns:
            command: such as +, -, EXIT etc
            params: the parameters of the command
        """
        return tcp_by_size.recv_by_size(self.client_socket)

    def send_response_to_client(self, response: str) -> None:
        """Create a protocol which sends the response to the client

        The protocol should be able to handle short responses as well as files
        (for example when needed to send the screenshot to the client)
        """
        tcp_by_size.send_with_size(self.client_socket, response)

    def check_client_request(self, command: str, params: list[str]) -> bool:
        """Check if the params are good.

        Returns:
            valid: True/False
            error_msg: None if all is OK, otherwise some error message
        """
        self.logger.info("---- Function check_client_request Enter ----")

        is_valid = False

        if command == '+' or command == '-' or command == '/' or command == '*' or command == '**' or command == '%' or command == 'EXIT':
            is_valid = True
            self.logger.info("Command is a valid operation")

        for number in params:
            if not isdigit(number):
                is_valid = False
                self.logger.info("Param: '{number}' is not a number")
                break
        self.logger.info("Checked if parameters are numbers only")

        self.logger.info(
            f"---- Function check_client_request Exit - returning the result: {is_valid} for the request ----")
        return is_valid

    def handle_client_request(self, message: str) -> str:
        """Create the response to the client, given the command is legal and params are OK

        Returns:
            response: the requested data
        """
        self.logger.info("---- Function handle_client_request Enter ----")

        splitted_message = message.split("~")
        command: str = splitted_message[0].upper()
        del splitted_message[0]
        params: list[str] = splitted_message

        res: str = ""
        operation: MathOperation.__builtins__ = None

        if command == '+':
            operation = MathOperation.Addition()

        elif command == '-':
            operation = MathOperation.Subtraction()

        elif command == '/':
            operation = MathOperation.Division()

        elif command == '*':
            operation = MathOperation.Multiplication()

        elif command == '**':
            operation = MathOperation.Power()

        elif command == '%':
            operation = MathOperation.Modulation()

        elif command == 'EXIT':
            self.logger.info(
                "Received an EXIT command from the client - needs to disconnect")
            res = "EXIT"
        else:
            self.logger.info("Received an invalid command from the client")
            res = 'commend does not exist'

        if operation:
            self.logger.info(
                f"Executing the operation: {operation.__class__.__name__}")
            try:
                operation_answer = operation.operate(
                    int(params[0]), int(params[1]))
                res = self.create_successful_message(
                    operation.__class__.__name__, params, operation_answer)
                self.logger.info("Executed successfully")
            except Exception as e:
                res = self.create_unsuccessful_message(
                    operation.__class__.__name__, str(e))
                self.logger.info("Executed unsuccessfully")
                self.logger.error(self.create_unsuccessful_message(
                    operation.__class__.__name__))

        self.logger.info("---- Function handle_client_request Exit ----")
        return res
