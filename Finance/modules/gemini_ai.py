import asyncio, os
from telethon import events, Button
from Finance import client
from Finance.status import user
from Finance.modules.plugins.gemini import baca_transaksi_dokumen 
from Finance.database.transaksi_db import tambah_transaksi 

transaksi_pending = {}

@client.on(events.NewMessage(func=lambda e: e.photo or e.document))
async def file_transaksi(event):
    if not user(event):
        return

    await event.reply("🔎 Membaca dokumen/bukti transaksi...")

    file_path = await event.download_media()
    
    if not file_path:
        await event.reply("❌ Gagal mengunduh file.")
        return

    try:
        hasil = await asyncio.to_thread(baca_transaksi_dokumen, file_path)

        if isinstance(hasil, dict) and "error" in hasil:
            await event.reply(f"❌ Gagal memproses file: {hasil['error']}")
            return

        if not hasil or len(hasil) == 0:
            await event.reply("❌ Tidak ada data transaksi yang ditemukan.")
            return

        transaksi_pending[event.sender_id] = hasil

        pesan = f"🔎 **Ditemukan {len(hasil)} transaksi:**\n\n"
        
        total_nominal = 0
        for i, item in enumerate(hasil, 1):
            nominal = int(item.get('nominal', 0))
            total_nominal += nominal
            pesan += f"{i}. [{item.get('tipe', '-')}] {item.get('keterangan', '-')} — Rp {nominal:,}\n"

        pesan += f"\n**Total Nominal:** Rp {total_nominal:,}"
        pesan += "\n\nSimpan SEMUA transaksi ini?"

        await event.reply(
            pesan,
            buttons=[
                [
                    Button.inline(f"✅ Simpan Semua ({len(hasil)})", b"simpan"),
                    Button.inline("❌ Batal", b"batal")
                ]
            ]
        )

    except Exception as e:
        await event.reply(f"❌ Terjadi kesalahan: {e}")
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@client.on(events.CallbackQuery(data=b"simpan"))
async def simpan(event):
    if event.sender_id not in transaksi_pending:
        await event.answer("Tidak ada transaksi pending", alert=True)
        return

    daftar_transaksi = transaksi_pending[event.sender_id]
    saldo_akhir = 0
    jumlah_sukses = 0

    for item in daftar_transaksi:
        try:
            saldo_akhir = tambah_transaksi(
                item.get("tipe", "KELUAR"),
                item.get("kategori", "Umum"),
                int(item.get("nominal", 0)),
                item.get("keterangan", "-")
            )
            jumlah_sukses += 1
        except Exception as e:
            print(f"Gagal menyimpan 1 transaksi: {e}")

    del transaksi_pending[event.sender_id]

    await event.edit(
        f"""✅ **{jumlah_sukses} transaksi berhasil disimpan ke database!**

**Saldo sekarang:** Rp {saldo_akhir:,}"""
    )


@client.on(events.CallbackQuery(data=b"batal"))
async def batal(event):
    if event.sender_id in transaksi_pending:
        del transaksi_pending[event.sender_id]

    await event.edit("❌ Transaksi dibatalkan.")
