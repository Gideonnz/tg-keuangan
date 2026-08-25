from Finance import client
from telethon import events, Button

START_TEXT = """
**Hi [{}](tg://user?id={})!**

Aku adalah Bot Pencatat Keuangan Kamu
Saya Bisa Mencatat Pengeluaran dan Pemasukan Anda Dari Ketikan dan Gambar.

Klik Tombol Di Bawah Ini Untuk Menu Bantuan.
"""

@client.on(events.NewMessage(pattern=r"^[/.!]start"))
async def start(event):

    if not user(event):
        return


    await event.respond(START_TEXT.format(event.sender.first_name, event.sender_id),
        buttons=[[Button.inline("Bantuan", data="bantuan1")]]
                       )
