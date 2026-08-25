import asyncio
from telethon import events, Button
from Finance import client
from Finance.status import user
from Finance.modules.plugins.gemini import baca_transaksi_gambar
from Finance.database.transaksi import tanbah_transaksi 

transaksi_pending = {}

@client.on(events.NewMessage(func=lambda e: e.photo))
async def foto_transaksi(event):
    if not user(event):
        return

    await event.reply("🔎 Membaca bukti transaksi...")

    file = await event.download_media(file="bukti.jpg")

    try:
        hasil = await asyncio.to_thread(baca_transaksi_gambar, file)

        if "error" in hasil:
            await event.reply(f"❌ Gagal memproses gambar: {hasil['error']}")
            return

        transaksi_pending[event.sender_id] = hasil

        await event.reply(
            f"""🔎 Hasil pembacaan AI:

Jenis: {hasil.get('tipe', '-')}
Kategori: {hasil.get('kategori', '-')}
Nominal: Rp {int(hasil.get('nominal', 0)):,}
Keterangan: {hasil.get('keterangan', '-')}

Simpan transaksi ini?""",
            buttons=[
                [
                    Button.inline("✅ Simpan", b"simpan"),
                    Button.inline("❌ Batal", b"batal")
                ]
            ]
        )

    except Exception as e:
        await event.reply(f"Gagal membaca gambar: {e}")


@client.on(events.CallbackQuery(data=b"simpan"))
async def simpan(event):
    if event.sender_id not in transaksi_pending:
        await event.answer("Tidak ada transaksi pending", alert=True)
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
        f"""✅ Transaksi berhasil disimpan.

Jenis: {data['tipe']}
Kategori: {data['kategori']}
Nominal: Rp {int(data['nominal']):,}
Keterangan: {data['keterangan']}

Saldo sekarang: Rp {saldo:,}"""
    )


@client.on(events.CallbackQuery(data=b"batal"))
async def batal(event):
    if event.sender_id in transaksi_pending:
        del transaksi_pending[event.sender_id]

    await event.edit("❌ Transaksi dibatalkan.")
