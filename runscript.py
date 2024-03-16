import threading
import time
from multiprocessing import Process, Manager
import queue
import rob

print("what about here?")
def start_server(queue):
    # Import the webcontrol app here, after the queue has been initialized
    from newWebControl import app
    app.queue = queue  # Set the queue attribute of the app

    import uvicorn
    # Start the FastAPI server in a separate thread
    uvicorn.run(app, host='0.0.0.0', port=9000)
    time.sleep(2)

def start_socket(queue):
    import server
    server.main(queue)

def start_face(rob_instance):
    face = rob_instance.get_robot_face()
    print("testing something")
    face.initialize_pygame()
    face.animate_eyes()
    print("testing if that something somethinged")
    return rob_instance

if __name__ == "__main__":
    with Manager() as manager:
        queue = manager.Queue()
        rob_instance = rob.get_rob_instance(queue)
        rob_instance.set_queue(queue)

        server_process = Process(target=start_server, args=(queue,))
        server_process.start()

        socket_process = Process(target=start_socket, args=(queue,))
        socket_process.start()

        start_face(rob_instance)

        socket_process.join()
        server_process.join()
