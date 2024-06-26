from ClientActions import ClientActions
from MyLogger import MyLogger


def main():
    # open socket with the server
    logger.info("Connecting to server")
    client_actions = ClientActions()
    client_actions.connect_client()

    # print instructions
    print('\nWelcome to remote computer application. Available commands are:\n')
    print('+\n-\n/\n*\n**\n%')
    print("please send requests in this format: operation~number~number")
    print("or simply send EXIT to finish")

    done = False
    # loop until user requested to exit
    try:
        while not done:
            logger.info("Getting a command from the user")
            request = input("Please enter command:\n")  # .upper()
            if client_actions.is_request_valid(request):
                client_actions.send_request_to_server(request)
                client_actions.print_server_response()
                if request.upper() == 'EXIT':
                    done = True
            else:
                print('can not send this request - invalid')
        logger.info("Disconnecting from the server")
        client_actions.connect_client()
    except Exception as e:
        logger.info('The server has fallen \nGOODBYE!!!')
        if e:
            logger.error("Error Message: " + str(e))


if __name__ == '__main__':
    logger = MyLogger()
    main()
