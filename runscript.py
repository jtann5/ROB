import threading
import asyncio
from rob import rob
from webControl import run_flask
import multiprocessing
import server

async def start_server():
    await run_flask()

def start_socket():
    server.main()

if __name__ == "__main__":
    # Start the face thread
    face_thread = threading.Thread(target=rob.start_face)
    face_thread.start()

    # Start the server socket process
    #socket_process = multiprocessing.Process(target=start_socket)
    # socket_process.start()

    # Start the Flask server asynchronously
    asyncio.run(start_server())

    # Wait for the face thread and server socket process to finish
    face_thread.join()
    # socket_process.join()




'''
import threading
import asyncio
from rob import rob
from webControl import run_flask

async def start_server():
    await run_flask()

def start_socket():
    import server
    server.main()


if __name__ == "__main__":
    face_thread = threading.Thread(target=rob.start_face)
    face_thread.start()
    #socket_thread = threading.Thread(target=start_socket)
    #socket_thread.start()

    asyncio.run(start_server())
    # rob.say("I love code")
    #socket_thread.join()
    face_thread.join()
'''