from telethon import events
from Finance import client
from Finance.status import user
from Finance.database.laporan_db import ambil_laporan_bulan

@client.on(events.NewMessage(pattern="^[/.!]laporan"))
async def laporan(event, send_id):

    if not user(event):
        return


    masuk, keluar = ambil_laporan_bulan(send_id)

    saldo = masuk - keluar


    await event.reply(
f"""
Laporan Bulan Ini

Pemasukan:
Rp {masuk:,}

Pengeluaran:
Rp {keluar:,}

Saldo:
Rp {saldo:,}
"""
    )
