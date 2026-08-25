from telethon import events
from Finance import client
from Finance.status import user
from Finance.database.saldo_db import atur_saldo_awal

@client.on(events.NewMessage(pattern="^[/.!]saldo_awal"))
async def saldo_awal(event):

    if not user(event):
        return


    try:

        data = event.raw_text.split()


        nominal = int(data[1])


        atur_saldo_awal(
            nominal
        )


        await event.reply(
f"""
Saldo awal berhasil dibuat.

Saldo awal:
Rp {nominal:,}
"""
        )


    except:

        await event.reply(
"""
Format:

/saldo 1000000

Contoh:
/saldo 5000000
"""
        )
