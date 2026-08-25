import sqlite3

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
        keterangan TEXT,
        saldo_setelah INTEGER
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pengaturan (
        id INTEGER PRIMARY KEY,
        saldo_awal INTEGER
    )
    """)


    conn.commit()
    conn.close()
