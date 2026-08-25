from datetime import datetime
from . import koneksi
from .saldo import saldo_sekarang, hitung_ulang_saldo

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

def hapus_transaksi(id_transaksi):

    conn = koneksi()
    cursor = conn.cursor()


    cursor.execute("""
    DELETE FROM transaksi
    WHERE id=?
    """,
    (
        id_transaksi,
    ))


    berhasil = cursor.rowcount > 0


    conn.commit()
    conn.close()


    if berhasil:
        hitung_ulang_saldo()


    return berhasil


def total_transaksi():

    conn = koneksi()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT COUNT(*)
    FROM transaksi
    """)


    total = cursor.fetchone()[0]


    conn.close()

    return total
