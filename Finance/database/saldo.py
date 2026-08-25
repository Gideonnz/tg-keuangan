from . import koneksi

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


def hitung_ulang_saldo():

    conn = koneksi()
    cursor = conn.cursor()


    # Ambil saldo awal
    cursor.execute("""
    SELECT saldo_awal
    FROM pengaturan
    WHERE id=1
    """)

    data = cursor.fetchone()


    saldo = 0

    if data:
        saldo = data[0]


    cursor.execute("""
    SELECT id, tipe, nominal
    FROM transaksi
    ORDER BY id ASC
    """)


    transaksi = cursor.fetchall()


    for id, tipe, nominal in transaksi:

        if tipe == "MASUK":
            saldo += nominal

        else:
            saldo -= nominal


        cursor.execute("""
        UPDATE transaksi
        SET saldo_setelah=?
        WHERE id=?
        """,
        (
            saldo,
            id
        ))


    conn.commit()
    conn.close()
