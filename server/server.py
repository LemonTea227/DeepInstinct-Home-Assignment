from ServerActions import ServerActions
from MyLogger import MyLogger


def main():
    while True:
        server_actions = ServerActions()
        server_actions.connect_server()

        # handle requests until user asks to exit
        done = False
        try:
            while not done:
                logger.info("Receiving a command from the client")
                str_message: str = server_actions.receive_client_request()  # type: ignore
                response = server_actions.handle_client_request(str_message)

                if response == 'EXIT':
                    done = True
                    server_actions.send_response_to_client(
                        "disconnecting you \nGOODBYE!!!")
                    logger.info("Disconnecting the client from the server")
                    server_actions.client_socket.close()
                else:
                    server_actions.send_response_to_client(response)

            server_actions.server_socket.close()
        except Exception as e:
            logger.info("Disconnecting the client from the server")
            server_actions.disconnect_server()
            if e:
                logger.error("Error Message: " + str(e))
            main()


if __name__ == '__main__':
    logger = MyLogger()
    main()
