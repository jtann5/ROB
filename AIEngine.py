from openai import OpenAI
import time

# You need to export environment variable OPENAI_API_KEY

# Micheal Scott, Mafia Boss, SpongeBob, Average US citizen, HAL but even creepier
MICHAEL_ID = 'asst_Qj2bNFAxYhjddMooeMg0MbkG'
MAFIA_ID = 'asst_2bm8X3fhBrmTBrz5YuRQFm2G'
SPONGEBOB_ID = 'asst_5iS33j8lokoYE5So2ccJmVKN'
REDNECK_ID = 'asst_QgfNpVmB7oY1mmxLwEACnNyp'
HAL_ID = 'asst_hGCh7jVelUJcFQFOuZHZ9nB1'

class AIEngine():
  def __init__(self):
    self.ASSISTANT_ID = ''
    self.select_assistant()
    self.client = OpenAI()
    self.thread = self.client.beta.threads.create()

  def select_assistant(self):
    print("0: Micheal Scott, 1: Mafia Boss, 2: SpongeBob SquarePants, 3: Redneck, 4: HAL")
    val = int(input("Enter number for assistant you want: "))
    self.set_assistant(val)

  def set_assistant(self, val):
    if val == 0:
      self.ASSISTANT_ID = MICHAEL_ID
      print("Michael Scott selected")
    elif val == 1:
      self.ASSISTANT_ID = MAFIA_ID
      print("Mafia Boss selected")
    elif val == 2:
      self.ASSISTANT_ID = SPONGEBOB_ID
      print("SpongeBob SquarePants selected")
    elif val == 3:
      self.ASSISTANT_ID = REDNECK_ID
      print("Redneck selected")
    elif val == 4:
      self.ASSISTANT_ID = HAL_ID
      print("HAL selected")

  def analyze(self, text):
    if text.lower() == 'change':
      self.select_assistant()
      return ''
    # Add message to a thread
    message = self.client.beta.threads.messages.create(
        thread_id=self.thread.id,
        role="user",
        content=text,
    )

    # Create a run
    run = self.client.beta.threads.runs.create(
      thread_id=self.thread.id,
      assistant_id=self.ASSISTANT_ID,
    )
      
    # Check for status of run
    while run.status in ['queued', 'in_progress', 'cancelling']:
      time.sleep(1) # Wait for 1 second
      run = self.client.beta.threads.runs.retrieve(
        thread_id=self.thread.id,
        run_id=run.id
      )

    # return message
    if run.status == 'completed': 
      message_response = self.client.beta.threads.messages.list(
        thread_id=self.thread.id
      )
      messages = message_response.data
      latest_message = messages[0]

      return latest_message.content[0].text.value
    else:
      return run.status