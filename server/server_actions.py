from curses.ascii import isdigit
import socket
import tcp_by_size
from math_operations.math_operation import MathOperation
from math_operations.addition import Addition
from math_operations.subtraction import Subtraction
from math_operations.multiplication import Multiplication
from math_operations.division import Division
from math_operations.power import Power
from math_operations.modulation import Modulation
from my_logger import MyLogger

IP = "0.0.0.0"
PORT = 22073

OPERATIONS_MAP: dict[str, MathOperation] = {
    "+": Addition(),
    "-": Subtraction(),
    "/": Division(),
    "*": Multiplication(),
    "**": Power(),
    "%": Modulation(),
}


logger = MyLogger()


class ServerActions:
    def __init__(self):
        self.server_socket: socket.socket = None  # type: ignore
        self.client_socket: socket.socket = None  # type: ignore
        self.address: socket._RetAddress = None  # type: ignore

    @logger.log_function
    def connect_server(self):
        """
        Opens a new socket connection to the client
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen(1)
        self.client_socket, self.address = self.server_socket.accept()

    @logger.log_function
    def disconnect_server(self):
        """
        Closes the socket connection to the client
        """
        self.client_socket.close()
        self.server_socket.close()

    @logger.log_function
    def create_successful_message(
        self, operation_name: str, params: list[str], answer: str
    ):
        message = (
            f"{operation_name} of {params[0]} and" f" {params[1]} result is: \n{answer}"
        )
        return message

    @logger.log_function
    def create_unsuccessful_message(
        self, operation_name: str, error_message: str = ""
    ) -> str:
        message = f"{operation_name} didn't work: \n{error_message}"
        return message

    @logger.log_function
    def receive_client_request(self) -> str:
        """
        Receives the full message sent by the client
        Works with the protocol defined in the client's
         "send_request_to_server" function

        :return: received data
        """
        return tcp_by_size.recv_by_size(self.client_socket).decode()

    @logger.log_function
    def send_response_to_client(self, response: str) -> None:
        """
        Create a protocol which sends the response to the client

        The protocol should be able to handle short responses as well as files
        (for example - when needed to send the screenshot to the client)
        """
        tcp_by_size.send_with_size(self.client_socket, response)

    @logger.log_function
    def validate_client_request(self, command: str, params: list[str]) -> bool:
        """
        Check if the params are good.

        :param command: command received
        :param params: the parameters of the command
        :return: is valid
        """
        is_valid = False

        if command in OPERATIONS_MAP:
            is_valid = True
            logger.info("Command is a valid operation")

        for number in params:
            if not isdigit(number):
                is_valid = False
                logger.info("Param: '{number}' is not a number")
                break
        logger.info("Checked if parameters are numbers only")

        logger.info(f"returning the result: {is_valid} for the request")
        return is_valid

    @logger.log_function
    def handle_client_request(self, message: str) -> str:
        """
        Create the response to the client,
        given the command is legal and params are OK

        Returns:
            response: the requested data
        """
        splitted_message: list[str] = message.split("~")
        command: str = splitted_message[0].upper()
        del splitted_message[0]
        params: list[str] = splitted_message

        res: str = ""

        if command in OPERATIONS_MAP:
            operation: MathOperation = OPERATIONS_MAP[command]
            logger.info(f"Executing the operation: {operation.__class__.__name__}")
            try:
                operation_answer = operation.operate(float(params[0]), float(params[1]))
                res = self.create_successful_message(
                    operation.__class__.__name__, params, str(operation_answer)
                )
                logger.info("Executed successfully")
            except Exception as e:
                res = self.create_unsuccessful_message(
                    operation.__class__.__name__, str(e)
                )
                logger.info("Executed unsuccessfully")
                logger.error(
                    self.create_unsuccessful_message(operation.__class__.__name__)
                )

        elif command == "EXIT":
            logger.info(
                "Received an EXIT command from the client - needs to disconnect"
            )
            res = "EXIT"
        else:
            logger.info("Received an invalid command from the client")
            res = "command does not exist"

        return res
