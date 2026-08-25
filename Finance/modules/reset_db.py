from telethon import events, Button
from Finance import client
from Finance.status import user
from Finance.database.reset_db import reset_database, reset_data

@client.on(events.NewMessage(pattern="^[/.!]reset_db"))
async def reset_db(event):

    if not user(event):
        return

    
    await event.reply("Apakah Anda yakin ingin mereset database?\n\nSetelah dihapus database tidak dapat dipulihkan lagi.",
         buttons=[[Button.inline("Reset Database", data="reset"), Button.inline("Batal", data="bbatal")]]
         )


@client.on(events.CallbackQuery(data="reset"))
async def breset(event):
    reset_database()

    await event.edit("""
       Database berhasil direset.

       Semua data dalam database telah di hapus.""")

@client.on(events.CallbackQuery(data="bbatal"))
async def bbatal(event):

    await event.edit("Aksi telah dibatalkan.")


@client.on(events.NewMessage(pattern="^[/.!]reset"))
async def reset(event):

    if not user(event):
        return

    
    await event.reply("Apakah Anda yakin ingin menghapus riwayat transaksi?",
         buttons=[[Button.inline("Reset Data", data="reset2"), Button.inline("Batal", data="bbatal2")]]
                     )


@client.on(events.CallbackQuery(data="reset2"))
async def breset2(event):
    reset_data()

    await event.reply("✅ Semua riwayat transaksi berhasil dihapus.")

@client.on(events.CallbackQuery(data="bbatal2"))
async def bbatal2(event):

    await event.reply("Aksi telah dibatalkan.")
