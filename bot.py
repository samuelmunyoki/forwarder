import asyncio
import logging

from config import API_HASH, API_ID, FORWARD_TO


from telethon import TelegramClient, events
from telethon.tl.custom.message import Message


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)


session_string= "bot_login_session"

client = TelegramClient(session_string, API_ID, API_HASH)
client.session.save()


@client.on(events.NewMessage( pattern='/ping'))
async def _(e):
    # Say "!pong" whenever you send "!ping", then delete both messages.
    m = await e.respond('🏓 Pong.')
    await asyncio.sleep(10)
    await client.delete_messages(e.chat_id, [e.id, m.id])
# incoming=True, outgoing=False
@client.on(events.NewMessage(incoming=True, outgoing=False))
async def _(e: Message):
    try:
        if e.document :
            if e.file.ext == ".zip" or e.file.ext == ".rar" or e.file.ext == ".7z":
                await client.send_message(entity=FORWARD_TO, message=e.raw_text, file=e.media)
    except Exception as ex:
            print(f"Error forwarding message: {ex}")

print("Bot forwarder activated.")
client.start()
client.run_until_disconnected()