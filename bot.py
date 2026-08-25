import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from database import (
    buat_database,
    tambah_transaksi,
    ambil_laporan_bulan
)

from excel_export import buat_excel

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context):

    await update.message.reply_text(
        """
Halo! Saya Bot Keuangan Pribadi.

Perintah:

/masuk nominal kategori keterangan

Contoh:
 /masuk 1000000 Gaji Gaji bulanan

/keluar nominal kategori keterangan

Contoh:
 /keluar 50000 Makanan Makan siang

/laporan
Melihat saldo bulan ini

/rekap_excel
Download laporan Excel
        """
    )

async def masuk(update: Update, context):

    await simpan(
        update,
        context,
        "MASUK"
    )

async def keluar(update: Update, context):

    await simpan(
        update,
        context,
        "KELUAR"
    )

async def simpan(update, context, tipe):

    try:

        nominal = int(
            context.args[0]
        )

        kategori = context.args[1]

        keterangan = " ".join(
            context.args[2:]
        )

        tambah_transaksi(
            tipe,
            kategori,
            nominal,
            keterangan
        )

        await update.message.reply_text(
            f"""
Transaksi berhasil disimpan.

Jenis:
{tipe}

Kategori:
{kategori}

Nominal:
Rp {nominal:,}
"""
        )

    except:

        await update.message.reply_text(
            """
Format salah.

Contoh:

/masuk 1000000 Gaji Gaji bulanan

/keluar 50000 Makanan Makan siang
"""
        )

async def laporan(update, context):

    masuk, keluar = ambil_laporan_bulan()

    saldo = masuk - keluar

    await update.message.reply_text(
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

async def rekap_excel(update, context):

    file = buat_excel()

    await update.message.reply_document(
        document=open(file,"rb"),
        filename=file
    )

def main():

    buat_database()

    app = Application.builder().token(
        TOKEN
    ).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "masuk",
            masuk
        )
    )

    app.add_handler(
        CommandHandler(
            "keluar",
            keluar
        )
    )

    app.add_handler(
        CommandHandler(
            "laporan",
            laporan
        )
    )

    app.add_handler(
        CommandHandler(
            "rekap_excel",
            rekap_excel
        )
    )

    print(
        "Bot berjalan..."
    )

    app.run_polling()

if __name__=="__main__":
    main()
