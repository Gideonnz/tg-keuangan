import os
from dotenv import load_dotenv

from telethon import TelegramClient, events, Button

from database import (
    buat_database,
    tambah_transaksi,
    ambil_laporan_bulan,
    atur_saldo_awal,
    hapus_transaksi,
    reset_database
)

from excel_export import buat_excel


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("USER_ID"))
client = TelegramClient(
    "tgbot",
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
    ).start(bot_token=TOKEN
)

# -------------------------------------------------

START_TEXT = """
**Hi [{}](tg://user?id={})!**

Aku adalah Bot Pencatat Keuangan Kamu
Saya Bisa Mencatat Pengeluaran dan Pemasukan Anda Hanya Dari Ketikan.

Klik Tombol Di Bawah Ini Untuk Menu Bantuan.
"""

HELP_TEXT = """
Daftar Perintah:

/saldo
Mengatur Saldo Awal

/in nominal kategori keterangan
Mencatat pemasukan.

/out nominal kategori keterangan
Mencatat pengeluaran.

/laporan
Berisi laporan keuangan selama sebulan.

/excel
Recap keuangan dalam bentuk excel.

/hapus_transaksi
Menghapus pengeluaran/pemasukan yang diinput.

/reset_db
Memghapus semua data di database.
"""

def user(event):

    return event.sender_id == USER_ID



@client.on(events.NewMessage(pattern=r"^[/.!]start"))
async def start(event):

    if not user(event):
        return


    await event.respond(START_TEXT.format(event.sender.first_name, event.sender_id),
        buttons=[[Button.inline("Bantuan", data="bantuan")]]
)

@client.on(events.NewMessage(pattern=r"^[/.!]help"))
async def help(event):
    
    if not user(event):
        return
    
   
    await event.respond(HELP_TEXT,
        buttons=[[Button.inline("Kembali", data="kembali")]]
                     )

@client.on(events.callbackquery.CallbackQuery(data="kembali"))
async def bstart(event):
     await event.edit(START_TEXT.format(event.sender.first_name, event.sender_id),
            buttons=[[Button.inline("Bantuan", data="bantuan")]]
                     )


@client.on(events.callbackquery.CallbackQuery(data="bantuan"))
async def bhelp(event):
     await event.edit(HELP_TEXT,
            buttons=[[Button.inline("Kembali", data="kembali")]]
                     )



@client.on(events.NewMessage(pattern=r"^[/.!]in"))
async def masuk(event):

    if not user(event):
        return


    await simpan(
        event,
        "MASUK"
    )



@client.on(events.NewMessage(pattern=r"^[/.!]out"))
async def keluar(event):

    if not user(event):
        return


    await simpan(
        event,
        "KELUAR"
    )



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

@client.on(events.NewMessage(pattern="^[/.!]laporan"))
async def laporan(event):

    if not user(event):
        return


    masuk, keluar = ambil_laporan_bulan()

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


@client.on(events.NewMessage(pattern=r"^[/.!]reset_db"))
async def reset_db(event):

    if not user(event):
        return


     await event.reply("Apakah Anda yakin ingin mereset database?\n\nSetelah dihapus database tidak dapat dipulihkan lagi.",
            buttons=[[Button.inline("Reset Database", data="reset", Button.inline("Batal", data="batal"))]]
                     )


@client.on(events.callbackquery.CallbackQuery(data="reset"))
async def breset(event):
    reset_database()

    await event.edit("""Database berhasil direset

                     Semua transaksi dan saldo telah di hapus.""")


@client.on(events.callbackquery.CallbackQuery(data="batal"))
async def bbatal(event):

    await event.edit("Aksi telah dibatalkan.")


def main():
    buat_database()
    print("Bot Bekerja Dengan Baik.")

    client.start()
    client.run_until_disconnected()



if __name__=="__main__":
    main()
