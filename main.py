import os
from dotenv import load_dotenv

from telethon import TelegramClient, events, Button

from database import (
    buat_database,
    tambah_transaksi,
    ambil_laporan_bulan
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

/in nominal kategori keterangan
Mencatat pemasukan.

/out nominal kategori keterangan
Mencatat pengeluaran.

/laporan
Berisi laporan keuangan selama sebulan.

/excel
Recap keuangan dalam bentuk excel.
"""

def user(event):

    return event.sender_id == USER_ID



@client.on(events.NewMessage(pattern=r"^[/.!]start"))
async def start(event):

    if not user(event):
        return


    await event.reply(START_TEXT.format(event.sender.first_name, event.sender_id),
        buttons=[[Button.inline("Bantuan", data="bantuan")]]
)

@client.on(events.NewMessage(pattern=r"^[/.!]help"))
async def help(event):
    
    if not user(event):
        return
    
   
    await event.reply(HELP_TEXT,
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


        tambah_transaksi(
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




def main():
    buat_database()
    print("Bot Bekerja Dengan Baik.")

    client.start()
    client.run_until_disconnected()



if __name__=="__main__":
    main()
