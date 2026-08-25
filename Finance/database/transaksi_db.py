from datetime import datetime
from . import koneksi
from .saldo_db import saldo_sekarang, hitung_ulang_saldo

def tambah_transaksi(
    user_id,
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
    user_id,
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
        user_id,
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


def cek_transaksi(id_transaksi):

    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        tanggal,
        tipe,
        kategori,
        nominal,
        keterangan,
        saldo_setelah
    FROM transaksi
    WHERE id=? AND user_id=?
    """,
    (id_transaksi,))


    data = cursor.fetchone()

    conn.close()

    return data



def semua_transaksi():

    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        tanggal,
        tipe,
        kategori,
        nominal,
        keterangan,
        saldo_setelah
    FROM transaksi
    WHERE user_id=?
    ORDER BY id ASC
    """)

    cursor.execute(
    query,
    (user_id,)
    )

    data = cursor.fetchall()

    conn.close()

    return data

def hapus_transaksi(id_transaksi):

    conn = koneksi()
    cursor = conn.cursor()


    cursor.execute("""
    DELETE FROM transaksi
    WHERE id=? AND user_id=?
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


def edit_transaksi(
    id_transaksi,
    tipe,
    kategori,
    nominal,
    keterangan
):

    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE transaksi
    SET
        tipe=?,
        kategori=?,
        nominal=?,
        keterangan=?
    WHERE id=? AND user_id=?
    """,
    (
        tipe,
        kategori,
        nominal,
        keterangan,
        id_transaksi
    ))

    berhasil = cursor.rowcount > 0

    conn.commit()
    conn.close()


    if berhasil:
        hitung_ulang_saldo()


    return berhasil
