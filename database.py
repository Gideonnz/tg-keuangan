import sqlite3
from datetime import datetime

DB_NAME = "keuangan.db"

def koneksi():
    return sqlite3.connect(DB_NAME)

def buat_database():

    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tanggal TEXT,
        tipe TEXT,
        kategori TEXT,
        nominal INTEGER,
        keterangan TEXT
    )
    """)

    conn.commit()
    conn.close()

def tambah_transaksi(tipe, kategori, nominal, keterangan):

    conn = koneksi()
    cursor = conn.cursor()

    tanggal = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
    INSERT INTO transaksi
    (tanggal, tipe, kategori, nominal, keterangan)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        tanggal,
        tipe,
        kategori,
        nominal,
        keterangan
    ))

    conn.commit()
    conn.close()

def ambil_laporan_bulan():

    conn = koneksi()
    cursor = conn.cursor()

    bulan = datetime.now().strftime("%Y-%m")

    cursor.execute("""
    SELECT tipe, SUM(nominal)
    FROM transaksi
    WHERE tanggal LIKE ?
    GROUP BY tipe
    """,
    (
        bulan+"%",
    ))

    data = cursor.fetchall()

    conn.close()

    pemasukan = 0
    pengeluaran = 0

    for tipe,total in data:

        if tipe=="MASUK":
            pemasukan = total

        else:
            pengeluaran = total

    return pemasukan, pengeluaran

def semua_transaksi():

    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT tanggal, tipe, kategori, nominal, keterangan
    FROM transaksi
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data