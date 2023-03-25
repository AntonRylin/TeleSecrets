from telethon import TelegramClient, events
from Replies import replies
import datetime
import os

# Log in information
api_id = 20370416
api_hash = '8a87367a3e969d4f52c4c4f90549ca38'
phone_number = '+4366499489619'
session_name = "ChatBot"

# client Init
client = TelegramClient(session_name, api_id, api_hash)

# configuration
auto_save = True  # True to treat all messages as save prompts
stealth = True  # True to provide no feedback


# define an event handler for incoming messages
@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    try:

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
                open(existing, "a").write(timestamp+message_body)
            except:
                open(existing, "w").write(timestamp+message_body)



        # reply / feedback
        if not stealth:
            await event.respond((replies[prompt]))

        # id
        print("Received a message from: "+str(event.message.sender_id)+" - "+" ".join(message_body.split()[0:10]))
        # delete the received message
        await client.delete_messages(event.chat_id, event.message)

    except:
        if not stealth:
            await event.respond("not understood, try 'help'")


# forever running
client.start()
client.run_until_disconnected()
