from telethon import events
from Finance.database.transaksi_db import tambah_transaksi



async def simpan(event, tipe):

    try:

        data = event.raw_text.split(
            " ",
            3
        )


        nominal = int(data[1])

        kategori = data[2]

        keterangan = data[3]


        saldo = tambah_transaksi(
          event.sender_id,
          tipe,
          kategori,
          nominal,
          keterangan
        )


        await event.reply(
f"""
Berhasil disimpan.

Jenis:
{tipe}

Kategori:
{kategori}

Nominal:
Rp {nominal:,}

Sisa Saldo:
Rp {saldo:,}
"""
)


    except:

        await event.reply(
"""
Format salah.

Contoh:

/masuk 100000 Gaji Bonus
"""
        )
