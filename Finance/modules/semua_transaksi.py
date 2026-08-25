from telethon import events, Button
from Finance import client
from Finance.status import user
from Finance.database.transaksi import semua_transaksi, hapus_transaksi, edit_transaksi

halaman_all = {}
edit_state = {}

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

    tombol.append(
    [
        Button.inline(
            "✏️ Edit",
            data=f"edit_{data[index][0]}".encode()
        ),

        Button.inline(
            "🗑 Hapus",
            data=f"delete_{data[index][0]}".encode()
        )
    ]
    )


    navigasi = []


    if index > 0:

        navigasi.append(
            Button.inline(
              "⬅️ Sebelumnya",
              data=f"prev_{index}".encode()
            )
        )


    if index < total - 1:

        navigasi.append(
            Button.inline(
              "➡️ Berikutnya",
              data=f"next_{index}".encode()
            )
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


@client.on(events.CallbackQuery(pattern=b"delete_"))
async def delete(event):

    id_transaksi = int(
        event.data.decode().split("_")[1]
    )


    await event.edit(
        "⚠️ Yakin ingin menghapus transaksi ini?",
        buttons=[
            [
                Button.inline(
                    "✅ Ya",
                    data=f"confirm_delete_{id_transaksi}".encode()
                ),

                Button.inline(
                    "❌ Batal",
                    data=b"cancel_delete"
                )
            ]
        ]
    )


@client.on(events.CallbackQuery(pattern=b"confirm_delete_"))
async def confirm_delete(event):

    id_transaksi = int(
        event.data.decode().split("_")[2]
    )


    berhasil = hapus_transaksi(
        id_transaksi
    )


    if berhasil:

        await event.edit(
            "✅ Transaksi berhasil dihapus."
        )

    else:

        await event.edit(
            "❌ Transaksi tidak ditemukan."
    )


@client.on(events.CallbackQuery(pattern=b"cancel_delete"))
async def cancel_delete(event):

    await event.edit(
        "❌ Penghapusan dibatalkan."
    )


@client.on(events.CallbackQuery(pattern=b"edit_"))
async def edit(event):

    id_transaksi = int(
        event.data.decode().split("_")[1]
    )

    edit_state[event.sender_id] = id_transaksi

    await event.respond(
"""
Kirim data baru.

Format:

JENIS NOMINAL KATEGORI KETERANGAN

Contoh:

MASUK 500000 GAJI Bonus bulanan
"""
)


@client.on(events.NewMessage)
async def proses_edit(event):

    user_id = event.sender_id

    if user_id not in edit_state:
        return


    try:

        data = event.raw_text.split(
            " ",
            3
        )


        tipe = data[0].upper()

        nominal = int(data[1])

        kategori = data[2]

        keterangan = data[3]


        id_transaksi = edit_state[user_id]


        berhasil = edit_transaksi(
            id_transaksi,
            tipe,
            kategori,
            nominal,
            keterangan
        )


        del edit_state[user_id]


        if berhasil:

            await event.reply(
                "✅ Transaksi berhasil diedit."
            )

        else:

            await event.reply(
                "❌ Gagal mengedit transaksi."
            )


    except:

        await event.reply(
"""
Format salah.

Contoh:

MASUK 500000 GAJI Bonus
"""
        )
