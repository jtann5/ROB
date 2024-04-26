from openai import OpenAI
from rob import rob
from threading import Thread
import time


# You need to export environment variable OPENAI_API_KEY
client = OpenAI()

# Create a thread
thread = client.beta.threads.create()

def get_response(text):
  # Add message to a thread
  message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=text,
  )

  # Create a run
  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id='asst_nGq1hA5qk9t9LGrNYlFa9qPx',
  )
    
  # Check for status of run
  while run.status in ['queued', 'in_progress', 'cancelling']:
    time.sleep(1) # Wait for 1 second
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )

  # return message
  if run.status == 'completed': 
    message_response = client.beta.threads.messages.list(
      thread_id=thread.id
    )
    messages = message_response.data
    latest_message = messages[0]

    return latest_message.content[0].text.value
  else:
    return run.status
  
def run_speaking():
    rob.sayThread(get_response("Generate a speech on a random topic but not kindness"))
    while (rob.face.robot_state == 'talking'):
      rob.randomMovement()
      rob.smoothDefaults()


if __name__ == "__main__":
    speaking_thread = Thread(target=run_speaking)
    face_thread = Thread(target=rob.start_face)

    speaking_thread.start()
    face_thread.start()
    speaking_thread.join()
    face_thread.join()

