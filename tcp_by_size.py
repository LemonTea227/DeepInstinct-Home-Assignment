import socket
from my_logger import MyLogger

logger = MyLogger()

SIZE_OF_LEN: int = 7


@logger.log_function
def send_with_size(sock: socket.socket, data: bytes | str) -> None:
    """
    sends a message with size, to make sure the message is received on the
     other side of the socket with all its contents

    :param sock: the socket used to send the data on.
    :param data:the data to send.
    """
    data_to_send: bytes | str
    encoded_data = bytes(data)  # type: ignore

    data_to_send = str(len(encoded_data)).zfill(SIZE_OF_LEN).encode() + encoded_data
    logger.info(
        "Built a message to send with size appended to the" " data - in bytes format"
    )
    sock.send(data_to_send)
    logger.info("Message sent to the socket")


@logger.log_function
def recv_by_size(sock: socket.socket) -> bytes:
    """
    receive the full message with size from the socket, to
      make sure its all received

    Args:
        sock: the socket used to receive the data on.
        is_bytes: is the data of bytes type.

    Returns:
        the fully received data from the socket by the declared format.
    """

    len_data: bytes = b""
    logger.info(
        f"Start receiving data until the size matches the length of"
        f" SIZE_OF_LEN field of the message which is: {SIZE_OF_LEN}"
    )
    while len(len_data) < SIZE_OF_LEN:
        len_data += sock.recv(SIZE_OF_LEN)
        if len(len_data) == 0:
            logger.info("returning an empty result")
            return b""
        int_len_data = int(len_data.decode())
        logger.info(
            f"Received the data required to determine the size of message we expect to receive which is: {int_len_data}"
        )
        data = b""
        logger.info(
            f"Now receiving data to append to the message by the size required: {int_len_data}"
        )
        while len(data) < int_len_data:
            new_data = sock.recv(int_len_data)
            data += new_data
            if data == "":
                logger.info("returning empty result")
                return b""

        logger.info("Message received")

    logger.info("returning the decoded message data")
    return data
