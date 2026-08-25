from telethon import events
from Finance import client
from Finance.status import user
from .plugins.gemini import baca_transaksi_gambar

transaksi_pending = {}

@client.on(events.NewMessage(func=lambda e: e.photo))
async def foto_transaksi(event):

    if not user(event):
        return


    await event.reply("🔎 Membaca bukti transaksi...")


    file = await event.download_media(file="bukti.jpg")


    try:

        hasil = baca_transaksi_gambar(file)
        transaksi_pending[event.sender_id] = hasil

        await event.reply(
f"""
🔎 Hasil pembacaan AI:

Jenis:
{hasil["tipe"]}

Kategori:
{hasil["kategori"]}

Nominal:
Rp {int(hasil["nominal"]):,}

Keterangan:
{hasil["keterangan"]}


Simpan transaksi ini?
""",
            buttons=[
                [
                    Button.inline("✅ Simpan", "simpan"),
                    Button.inline("❌ Batal", "batal")
                ]
            ]
        )


    except Exception as e:

        await event.reply(
            f"Gagal membaca gambar: {e}"
        )


@client.on(events.callbackquery.CallbackQuery(data="simpan"))
async def simpan(event):

    if event.sender_id not in transaksi_pending:

       await event.answer(
          "Tidak ada transaksi pending",
          alert=True
          )

       return


    data = transaksi_pending[event.sender_id]


    saldo = tambah_transaksi(
        data["tipe"],
        data["kategori"],
        int(data["nominal"]),
        data["keterangan"]
    )


    del transaksi_pending[event.sender_id]


    await event.edit(
f"""
✅ Transaksi berhasil disimpan.

Jenis:
{data["tipe"]}

Kategori:
{data["kategori"]}

Nominal:
Rp {int(data["nominal"]):,}

Keterangan:
{data["keterangan"]}

Saldo sekarang:
Rp {saldo:,}
"""
        )


@client.on(events.callbackquery.CallbackQuery(data="batal"))
async def batal(event):
  
    if event.sender_id in transaksi_pending:
      
      del transaksi_pending[event.sender_id]


    await event.edit("❌ Transaksi dibatalkan.")
