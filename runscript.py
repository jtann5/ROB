import threading
import time
from multiprocessing import Process, Queue

print("what about here?")
def start_server(queue):
    # Import the webcontrol app here, after the queue has been initialized
    from newWebControl import app
    app.queue = queue  # Set the queue attribute of the app

    import uvicorn
    # Start the FastAPI server in a separate thread
    uvicorn.run(app, host='0.0.0.0', port=9000)
    time.sleep(2)

def start_face(queue):
    import rob
    rob_instance = rob.get_rob_instance(queue)
    face = rob_instance.get_robot_face()
    print("testing something")
    face.initialize_pygame()
    face.animate_eyes()
    print("testing if that something somethinged")

if __name__ == "__main__":
    queue = Queue()

    server_process = Process(target=start_server, args=(queue,))
    server_process.start()

    start_face(queue)

    server_process.join()
