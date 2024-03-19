import sys
import socket
import pickle
import time
from rob import ROB

client_script = [
    "Hi, you look familiar.",
    "I am from Montana, where are you from?",
    "Me too, I am from the room we are in currently in Bozeman, Montana",
    "Tango",
    "What are the odds. Two robots run into each other from the same state, and the same town, and the same room, with the same name?",
    "eof",
]

has_token = False


def main():
    pc_instance = ROB()
    global has_token
    sleep_time = 1
    port = 8000
    host = '172.20.10.3'

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, port))

    try:
        rec = True
        index = 0
        client_eof = False
        server_eof = False
        while rec:
            if server_eof:
                has_token = True
            if has_token == True:
                # rob.say(server_script[index])
                if index <= len(client_script)-1:
                    if ("eof" == client_script[index]) or (len(client_script) == index-1):
                        clientSocket.send("eof".encode())
                        has_token = False
                        client_eof = True
                    else:
                        print(str(index) + " " + client_script[index])
                        pc_instance.say(client_script[index])
                        time.sleep(0.5)
                        index += 1
                        if server_eof == False:
                            clientSocket.send("token".encode())
                            has_token = False
                        else:
                            clientSocket.send("ack".encode())
                            has_token = True
            else:
                data = clientSocket.recv(1024).decode()
                if "token" == data:
                    has_token = True
                elif "eof" == data:
                    server_eof = True

            if client_eof and server_eof:
                rec = False
                break

    except Exception as e:
        print("Server Error: ", str(e))
    finally:
        clientSocket.close()


main()
