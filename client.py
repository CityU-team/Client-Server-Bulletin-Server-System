import os
import socket
import struct

BUFFER_SIZE = 128
ERROR_MESSAGE = "Error: connection is not built, try again"


def send_message(sock, message):
    sock.sendall(bytes(message, encoding='utf-8'))


def receive_message(sock):
    data = sock.recv(BUFFER_SIZE)
    return str(data, encoding='utf-8')


def post_string(sock):
    print("=============== Content (Type a lone '&' to end message) ===============")
    cnt = 0  # it counts the number of lines the client sends to the server
    send_message(sock, "POST_STRING")  # telling the server that the client entered POST_STRING
    while True:
        line = input("client: ")  # inputing the line the client sends
        cnt += 1
        send_message(sock, line)
        if line == "&":  # if the line is '&', we know the user should stop with the input
            break
    status = receive_message(sock)  # status that needs to be printed
    status_message = status.replace('server: ', '')
    server_address = sock.getsockname()  # obtaining the server's ip address and its port number
    print(f"{status}")
    print("---")
    print(f"Sent {cnt} messages to (IP address: {server_address[0]}, port number: {server_address[1]})")
    print(f"Connect status: {status_message}")
    print(f"Send status: {status_message}")
    print("---")


def post_file(sock):
    send_message(sock, "POST_FILE")  # telling the server that the client entered POST_FILE
    print(
        f"{receive_message(sock)}")  # receiving the message from the server requiring the client to send the
    # absolute path
    file_path = input("client: ")  # asking the client for the absolute path
    if os.path.isfile(file_path):  # checking whether the file path is correct or not
        print(f"Transfer file absolute path {file_path}")
        file_size = struct.calcsize('128sl')
        file_head = struct.pack('128sl', bytes(os.path.basename(file_path).encode('utf-8')), os.stat(
            file_path).st_size)  # creating the file header. packing the file name and size into binary format. the
        # file name is obtained and encoded as uft-8
        sock.send(file_head)  # sending the file header
        with open(file_path, 'rb') as fp:  # opening the file path in binary mode
            while True:
                data = fp.read()  # read the chunk of 1024 bytes
                # print(data)
                if not data:  # if nothing is read, then the code should terminate
                    break
                sock.send(data)  # send what has been read to the server
    else:
        print("Cannot find the file")
        sock.send(b"close")  # if we cannot find the file, we just send this

    status = receive_message(sock)  # obtaining the status
    print(f"{status}")


def get_messages(sock):
    send_message(sock, "GET")  # telling the server that the client entered GET
    print("---Received Messages---")
    response = receive_message(sock)
    while response != 'server: &':  # the last message is always & (the server sends it as 'server &'), that is how
        # we know it is the end. we cannot do response[-1] != & because the message we send can be abc& which is not
        # a sole character '&'
        print(
            f"{response.replace('server', 'client', 1)}")  # server sends the message in the format 'server: ...',
        # but the program needs to output 'client: ...'
        response = receive_message(sock)
    print(f"{response.replace('server', 'client', 1)}")
    server_address = sock.getsockname()  # obtaining the server ip address and the port number
    print(f"(IP address: {server_address[0]}, port number: {server_address[1]}) ")
    print(f"Connect status: OK")
    print(f"Send status: OK")


def main():
    while True:
        print("========================== Initialize socket ==========================")
        server_ip = input("input IP address : ")
        server_port = input("input port number: ")
        try:  # try checking whether it is possible to convert the input PORT number from string to integer
            server_port = int(server_port)
            try:  # try checking whether the connection can be established
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((server_ip, server_port))  #establishing connection

                first = True  # check whether the operation is first
                was_exit = False  # to stop the client if the command was 'EXIT'
                command_was = False  # check if the input command was right to send '====next command====' line
                while True:
                    if not command_was:
                        if first:  #Print this line before the
                            print("============================ Input command ============================")
                            first = False
                        else:
                            print("==============================next command=============================")
                        command_was = True
                    else:
                        command = input("Input command: ")
                        if command == "POST_STRING":
                            post_string(sock)
                            command_was = False
                        elif command == "POST_FILE":
                            post_file(sock)
                            command_was = False
                        elif command == "GET":
                            get_messages(sock)
                            command_was = False
                        elif command == "EXIT":
                            send_message(sock, "EXIT")
                            server_ok = receive_message(sock)  # receiving the OK from the server
                            print(server_ok)
                            was_exit = True
                            break
                        else:
                            print("ERROR - Command not understood")

                if was_exit:
                    break
            except:
                print(ERROR_MESSAGE)
        except:
            print(ERROR_MESSAGE)


if __name__ == "__main__":
    main()
