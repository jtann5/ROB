from openai import OpenAI

client = OpenAI()

# Define the initial conversation messages
initial_messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

# Start the conversation with the initial messages
conversation = initial_messages

# Continuously interact with the OpenAI Chat API
while True:
    # Ask for user input to continue the conversation
    user_input = input("Your message: ")

    # Add the user's input to the conversation
    user_message = {"role": "user", "content": user_input}
    conversation.append(user_message)

    # Generate response from OpenAI Chat API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=25
    )

    # Print the response
    message = response.choices[0].message.content

    print(message)
