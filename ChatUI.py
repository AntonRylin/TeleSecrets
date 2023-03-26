from telethon import TelegramClient, events
from Replies import replies
import datetime
import os
import threading


async def answer_console():
    reply = input("answering to " + str(last_id) + ": ")
    if reply:
        await client.send_message(last_id, reply)
        print("message sent to: " + str(last_id) + " - ", reply)


# Log in information
with open("credentials.txt", "r") as file:
    lines = file.readlines()
    api_id = int(lines[2].strip())
    api_hash = str(lines[3].strip())
    phone_number = str(lines[4].strip())

# client Init
client = TelegramClient('TeleSecrets', api_id, api_hash)

# configuration
auto_save = True  # True to treat all messages as save-prompts
stealth = True  # True to provide no feedback
console = False

# define an event handler for incoming messages
@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    #try:

        # index
        ind = 1

        # prompt
        message: str = event.message.text
        prompt: str = message.split()[0].lower()

        # auto save
        if auto_save:
            prompt = "save"
            ind = 0

        # setup
        id = event.message.sender_id
        global last_id

        last_id = id
        message_body = " ".join(message.split()[ind:])
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        existing = os.path.join("saved", str(id) + ".txt")
        timestamp = "\n" + now + ":\n"

        # stop bot option
        if prompt == "bye":
            await event.respond((replies[prompt]))
            client.disconnect()

        # save prompt
        if prompt == "save":

            try:
                open(existing, "a").write(timestamp + message_body)
            except:
                open(existing, "w").write(timestamp + message_body)

        # reply / feedback
        if not stealth:
            await event.respond((replies[prompt]))

        if console:
            # console: message received
            print("Received message from: " + str(event.message.sender_id) + " - " + " ".join(message_body.split()[0:10]))
        else:
            await client.send_message("me", "from "+str(id)+timestamp+message_body)

        # delete the received message from telegram
        await client.delete_messages(event.chat_id, event.message)

        if console:
            # awaiting response
            await answer_console()

    #except:
        if not stealth:
            await event.respond(replies["exception"])


# define an event handler for incoming messages
@client.on(events.NewMessage(incoming=False))
async def handle_new_message(event):
    await client.send_message(last_id, event.message.text)

# forever running
client.start()
client.run_until_disconnected()
