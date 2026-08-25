from telethon import events, Button
from Finance import client
from Finance.status import user
from Finance.database.reset_db import reset_database

@client.on(events.NewMessage(pattern="^[/.!]reset_db"))
async def reset_db(event):

    if not user(event):
        return

    
    await event.reply("Apakah Anda yakin ingin mereset database?\n\nSetelah dihapus database tidak dapat dipulihkan lagi.",
         buttons=[[Button.inline("Reset Database", data="reset"), Button.inline("Batal", data="batall")]]
         )


@client.on(events.callbackquery.CallbackQuery(data="reset"))
async def breset(event):
    reset_database()

    await event.edit("""Database berhasil direset

                     Semua transaksi dan saldo telah di hapus.""")

@client.on(events.callbackquery.CallbackQuery(data="batall"))
async def bbatal(event):

    await event.edit("Aksi telah dibatalkan.")
