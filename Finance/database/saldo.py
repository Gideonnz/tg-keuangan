from . import koneksi

def atur_saldo_awal(user_id, nominal):

    conn = koneksi()
    cursor = conn.cursor()


    cursor.execute("""
    INSERT INTO pengaturan
    (user_id, saldo_awal)
    VALUES (?, ?)

    ON CONFLICT(user_id)
    DO UPDATE SET saldo_awal=excluded.saldo_awal
    """,
    (
        user_id,
        nominal
    ))


    conn.commit()
    conn.close()


def saldo_sekarang(user_id):

    conn = koneksi()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT saldo_awal
    FROM pengaturan
    WHERE user_id=?
    """,
    (
        user_id,
    ))

    data = cursor.fetchone()


    saldo_awal = 0

    if data:
        saldo_awal = data[0]


    cursor.execute("""
    SELECT saldo_setelah
    FROM transaksi
    WHERE user_id=?
    ORDER BY tanggal DESC, id DESC
    LIMIT 1
    """,
    (
        user_id,
    ))


    terakhir = cursor.fetchone()


    conn.close()


    if terakhir:
        return terakhir[0]

    return saldo_awal


def hitung_ulang_saldo(user_id):

    conn = koneksi()
    cursor = conn.cursor()


    # Ambil saldo awal
    cursor.execute("""
    SELECT saldo_awal
    FROM pengaturan
    WHERE user_id=?
    """,
    (
        user_id,
    ))

    data = cursor.fetchone()


    saldo = 0

    if data:
        saldo = data[0]


    cursor.execute("""
    SELECT id, tipe, nominal
    FROM transaksi
    WHERE user_id=?
    ORDER BY tanggal ASC, id ASC
    """,
    (
        user_id,
    ))


    transaksi = cursor.fetchall()


    for transaksi_id, tipe, nominal in transaksi:

        if tipe == "MASUK":
            saldo += nominal

        else:
            saldo -= nominal


        cursor.execute("""
        UPDATE transaksi
        SET saldo_setelah=?
        WHERE id=? AND user_id=?
        """,
        (
            saldo,
            transaksi_id,
            user_id
        ))


    conn.commit()
    conn.close()

    return saldo
