from Finance import client
from telethon import events, Button

HELP_TEXT1 = """
Daftar Perintah:

/saldo
Mengatur Saldo Awal

/in nominal kategori keterangan
Mencatat pemasukan.

/out nominal kategori keterangan
Mencatat pengeluaran.

/scan
Gemini AI mencatat transaksi lewat analisis gambar.

/laporan
Berisi laporan keuangan selama sebulan.
"""

HELP_TEXT2 = """
Daftar perintah:

/excel
Recap keuangan dalam bentuk excel.

/hapus_transaksi
Menghapus pengeluaran/pemasukan yang diinput.

/reset_db
Memghapus semua data di database.

/cek_id
Cek transaksi berdasarkan ID.

/total_id
Jumlah seluruh transaksi.
"""

@client.on(events.NewMessage(pattern=r"^[/.!]help"))
async def help(event):
    
    if not user(event):
        return
    
   
    await event.respond(HELP_TEXT1,
        buttons=[
          [
            Button.inline("Kembali", data="kembali"),
            Button.inline("➡️", data="bantuan2")
          ]
        ]
                     )


@client.on(events.callbackquery.CallbackQuery(data="bantuan1"))
async def bhelp(event):
     await event.edit(HELP_TEXT1,
            buttons=
              [
                Button.inline("Kembali", data="kembali"),
                Button.inline("➡️", data="bantuan2")
              ]
          )

@client.on(events.callbackquery.CallbackQuery(data="bantuan2"))
async def bhelp(event):
     await event.edit(HELP_TEXT2,
            buttons=
              [
                Button.inline("⬅️", data="help1"),
                Button.inline("Kembali", data="kembali")
              ]
             )
