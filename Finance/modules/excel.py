from telthon import events
from Finance import client
from Finance.status import user
from Finance.database.excel import buat_excel

@client.on(events.NewMessage(pattern="^[/.!]excel"))
async def excel(event):

    if not user(event):
        return

    file = buat_excel()
    await client.send_file(
        event.chat_id,
        file,
        caption="Rekap Keuangan"
    )
