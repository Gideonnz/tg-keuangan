from datetime import datetime
from . import koneksi

def ambil_laporan_bulan():

    conn = koneksi()
    cursor = conn.cursor()

    bulan = datetime.now().strftime("%Y-%m")

    cursor.execute("""
    SELECT tipe, SUM(nominal)
    FROM transaksi
    WHERE user_id=?
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
