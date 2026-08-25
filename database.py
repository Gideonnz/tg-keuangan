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


def atur_saldo_awal(nominal):

    conn = koneksi()
    cursor = conn.cursor()


    cursor.execute(
        "DELETE FROM pengaturan"
    )


    cursor.execute("""
    INSERT INTO pengaturan
    (id, saldo_awal)
    VALUES (1, ?)
    """,
    (nominal,)
    )


    conn.commit()
    conn.close()


def saldo_sekarang():

    conn = koneksi()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT saldo_awal
    FROM pengaturan
    WHERE id=1
    """)

    data = cursor.fetchone()


    saldo_awal = 0

    if data:
        saldo_awal = data[0]


    cursor.execute("""
    SELECT saldo_setelah
    FROM transaksi
    ORDER BY id DESC
    LIMIT 1
    """)


    terakhir = cursor.fetchone()


    conn.close()


    if terakhir:
        return terakhir[0]

    return saldo_awal



def tambah_transaksi(
    tipe,
    kategori,
    nominal,
    keterangan
):

    conn = koneksi()
    cursor = conn.cursor()


    saldo = saldo_sekarang()


    if tipe == "MASUK":
        saldo += nominal

    else:
        saldo -= nominal



    tanggal = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute("""
    INSERT INTO transaksi
    (
    tanggal,
    tipe,
    kategori,
    nominal,
    keterangan,
    saldo_setelah
    )
    VALUES (?,?,?,?,?,?)
    """,
    (
        tanggal,
        tipe,
        kategori,
        nominal,
        keterangan,
        saldo
    ))


    conn.commit()
    conn.close()


    return saldo

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
