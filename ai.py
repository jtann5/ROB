from openai import OpenAI
import time

# Micheal Scott, Mafia Boss, SpongeBob, Average US citizen, HAL but even creepier
ASSISTANT_ID = 'asst_29gft1xsJgPoLMzosgaG5jBT' # Math Tutor
SPONGEBOB_ID = 'asst_z8zrKPv8RqXHyHDz5dxZ4JA9'
MICHAEL_ID = 'asst_Qj2bNFAxYhjddMooeMg0MbkG'
REDNECK_ID = 'asst_QgfNpVmB7oY1mmxLwEACnNyp'
HAL_ID = 'asst_hGCh7jVelUJcFQFOuZHZ9nB1'
MAFIA_ID = 'asst_2bm8X3fhBrmTBrz5YuRQFm2G'

def set_assistant(val):
  global ASSISTANT_ID

  if val == 0:
    ASSISTANT_ID = MICHAEL_ID
    print("Michael Scott selected")
  elif val == 1:
    ASSISTANT_ID = MAFIA_ID
    print("Mafia Boss selected")
  elif val == 2:
    ASSISTANT_ID = SPONGEBOB_ID
    print("SpongeBob SquarePants selected")
  elif val == 3:
    ASSISTANT_ID = REDNECK_ID
    print("Redneck selected")
  elif val == 4:
    ASSISTANT_ID = HAL_ID
    print("HAL selected")

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
    assistant_id=ASSISTANT_ID,
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


val = int(input("Enter number for assistant you want: "))
set_assistant(val)

while True:
  message = input("Enter a message: ")
  if message.lower() == 'exit': break
  print(get_response(message))