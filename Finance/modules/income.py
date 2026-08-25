from Finance import client
from telethon import events, Button
from Finance.modules.save import simpan

@client.on(events.NewMessage(pattern=r"^[/.!]in"))
async def masuk(event):
  
    if not user(event):
        return

    await simpan(event, "MASUK")
