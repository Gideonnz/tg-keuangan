from Finance import client
from Finance.status import user
from telethon import events
from Finance.modules.save import simpan

@client.on(events.NewMessage(pattern=r"^[/.!]out"))
async def keluar(event):

    if not user(event):
        return

    await simpan(event, "KELUAR")
