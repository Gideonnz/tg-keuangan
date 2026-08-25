from telethon import events
from Finance import client
from Finance.status import user
from Finance.database.transaksi import hapus transaksi

@client.on(events.NewMessage(pattern="^[/.!]hapus_transaksi"))
async def hapus(event):

    if not user(event):
        return


    try:

        data = event.raw_text.split()

        id_transaksi = int(data[1])


        hasil = hapus_transaksi(
            id_transaksi
        )


        if hasil:

            await event.respond(
f"""
Transaksi ID {id_transaksi} berhasil dihapus.
"""
            )

        else:

            await event.respond(
"""
ID transaksi tidak ditemukan.
"""
            )


    except:

        await event.respond(
"""
Format:

/hapus_transaksi ID

Contoh:

/hapus_transaksi 15
"""
        )
