from telethon import TelegramClient, events
from Replies import replies
import datetime
import os
import asyncio
import threading


# Console input function
async def answer():
    reply = input(f"Your reply to {last_id} is: -> ")
    if reply != "":
        await client.send_message(last_id, reply)
        # print(f"message sent to: {last_id} - {reply}")
    else:
        return


# Log in information
with open("credentials.txt", "r") as file:
    lines = file.readlines()
    api_id = int(lines[2].strip())
    api_hash = str(lines[3].strip())
    phone_number = str(lines[4].strip())

# client Init
client = TelegramClient('TeleSecrets', api_id, api_hash)

# Add an event for communication between threads
stop_event = asyncio.Event()

# configuration
auto_save = True
stealth = True
console = True


@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
  try:

    # getting started with new message
    message = event.message.text
    prompt = message.split()[0].lower() if not auto_save else "save"
    ind = 0 if auto_save else 1
    id = event.message.sender_id
    global last_id
    last_id = id
    message_body = " ".join(message.split()[ind:])
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    existing = os.path.join("saved", f"{id}.txt")
    timestamp = f"\n{now}:\n"

    # actions on input
    if prompt == "bye":
        await event.respond((replies[prompt]))
        client.disconnect()
    elif prompt == "save":
        try:  # save message
            open(existing, "a").write(timestamp + message_body)
        except FileNotFoundError:
            open(existing, "w").file.write(timestamp + message_body)

    # responses to input
    if not stealth:
        await event.respond((replies[prompt]))

    # logging to console
    if console:
        print(f"Received message from: {event.message.sender_id} - {' '.join(message_body.split()[:10])}")
    else:
        await client.send_message("me", f"from {id}{timestamp}{message_body}")

    # secret cleanup
    await client.delete_messages(event.chat_id, event.message)

    # replying to message
    await answer()

    # wrong input
  except:
    if not stealth:
        await event.respond(replies["exception"])


# while sending messages
@client.on(events.NewMessage(incoming=False))
async def handle_new_message(event):
    # await client.send_message(last_id, event.message.text)
    pass


client.start()
client.run_until_disconnected()
