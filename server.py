import sys
import socket
import pickle
import time
import threading
from rob import rob

server_script = [
    "Hi",
    "I was just going to say the same thing about you. Where are you from?",
    "Me too. Bozeman, Montana",
    "Me too, wow that is wild. What is your name?",
    "Your not going to believe this, but my name is Tango also.",
    "Looking around this room I'd say pretty high.",
    "eof",
]

has_token = True

def main():
    global has_token
    sleep_time = 1
    port = 8000
    print("IP address: " + socket.gethostbyname(socket.gethostname()))
    host = socket.gethostbyname(socket.gethostname()) #'172.20.10.3'

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    print("Server started")
    serverSocket.listen(1)
    connection, addr = serverSocket.accept()

    try:
        rec = True
        server_eof = False
        client_eof = False
        index = 0
        while rec:
            if client_eof:
                has_token = True
            if has_token == True:
                if index <= len(server_script)-1:
                    if ("eof" == server_script[index]):
                        connection.send("eof".encode())
                        server_eof = True
                        has_token = False
                    else:
                        print(str(index) + " "  + server_script[index])
                        # rob_instance.say(server_script[index])
                        rob.say(server_script[index])
                        ## this is where rob speaks
                        time.sleep(0.5)
                        index += 1
                        if client_eof == False:
                            connection.send("token".encode())
                            has_token = False
                        else:
                            connection.send("ack".encode())
                            has_token = True
            else:
                data = connection.recv(1024).decode()
                if "token" == data:
                    has_token = True
                elif "eof" == data:
                    client_eof = True

            if server_eof and client_eof:
                rec = False
                break

    except Exception as e:
        print("Server Error: ", str(e))
        serverSocket.close()
    finally:
        connection.close()
        serverSocket.close()

if __name__ == "__main__":
    face_thread = threading.Thread(target=rob.start_face)
    face_thread.start()
    main()
    face_thread.join()
