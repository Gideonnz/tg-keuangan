from telethon import events, Button
from Finance import client
from Finance.status import user
from Finance.database.transaksi import semua_transaksi

halaman_all = {}

def format_transaksi(data, nomor, total):

    (
        id,
        tanggal,
        tipe,
        kategori,
        nominal,
        keterangan,
        saldo
    ) = data


    return f"""
📒 Transaksi {nomor} dari {total}


ID:
{id}

Tanggal:
{tanggal}

Jenis:
{tipe}

Kategori:
{kategori}

Nominal:
Rp {nominal:,}

Keterangan:
{keterangan}

Saldo setelah:
Rp {saldo:,}
"""


async def tampilkan_semua(event, index, data):
    
  total = len(data)


    teks = format_transaksi(
        data[index],
        index + 1,
        total
    )


    tombol = []


    navigasi = []


    if index > 0:

        navigasi.append(
            Button.inline(
              "⬅️ Sebelumnya",
              data=f"prev_{index}".encode()
            )


    if index < total - 1:

        navigasi.append(
            Button.inline(
              "➡️ Berikutnya",
              data=f"next_{index}".encode()
            )


    if navigasi:

        tombol.append(
            navigasi
        )


    await event.reply(
        teks,
        buttons=tombol
    )


@client.on(events.NewMessage(pattern="^[.!/]all"))
async def all_transaksi(event):

    if not user(event):
        return


    data = semua_transaksi()


    if not data:

        await event.reply(
            "Belum ada transaksi."
        )

        return


    halaman_all[
        event.sender_id
    ] = 0


    await tampilkan_semua(
        event,
        0,
        data
    )


@client.on(events.CallbackQuery(pattern=b"next_"))
async def next(event):
  
    data = semua_transaksi()


    if not data:
        return


    index = int(
        event.data.decode().split("_")[1]
    )


    index += 1


    if index >= len(data):

        index = len(data)-1



    await event.edit(
        format_transaksi(
            data[index],
            index + 1,
            len(data)
        ),
        buttons=[
            [
                Button.inline(
                    "⬅️ Sebelumnya",
                    data=f"prev_{index}".encode()
                ),

                Button.inline(
                    "➡️ Berikutnya",
                    data=f"next_{index}".encode()
                )
            ]
        ]
)


@client.on(events.CallbackQuery(pattern=b"prev_"))
async def prev(event):

    data = semua_transaksi()


    if not data:
        return


    index = int(
        event.data.decode().split("_")[1]
    )


    index -= 1


    if index < 0:

        index = 0



    await event.edit(
        format_transaksi(
            data[index],
            index + 1,
            len(data)
        ),
        buttons=[
            [
                Button.inline(
                    "⬅️ Sebelumnya",
                    data=f"prev_{index}".encode()
                ),

                Button.inline(
                    "➡️ Berikutnya",
                    data=f"next_{index}".encode()
                )
            ]
        ]
)
