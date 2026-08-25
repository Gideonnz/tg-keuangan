from telethon import events
from Finance import client
from Finance.status import user
from Finance.database.transaksi_db import cek_transaksi, total_transaksi

@client.on(events.NewMessage(pattern="^[/.!]cek_id"))
async def cek_id(event):

    if not user(event):
        return


    try:

        data = event.raw_text.split()

        id_transaksi = int(data[1])


        transaksi = cek_transaksi(
            id_transaksi
        )


        if transaksi:


            (
                id,
                tanggal,
                tipe,
                kategori,
                nominal,
                keterangan,
                saldo
            ) = transaksi


            await event.reply(
f"""
Detail Transaksi

ID:
{id}

Tanggal:
{tanggal}

Tipe:
{tipe}

Kategori:
{kategori}

Nominal:
Rp {nominal:,}

Keterangan:
{keterangan}

Saldo Setelah:
Rp {saldo:,}
"""
            )


        else:

            await event.reply(
                "Transaksi tidak ditemukan."
            )


    except:

        await event.reply(
"""
Format:

/cek_id ID

Contoh:

/cek_id 10
"""
        )


@client.on(events.NewMessage(pattern="^[/.!]total_id"))
async def total_id(event):

    if not user(event):
        return


    jumlah = total_transaksi()


    await event.reply(
f"""
Total Transaksi:

Jumlah ID:
{jumlah}

ID terakhir:
{jumlah}
"""
)
