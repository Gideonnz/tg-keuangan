import pandas as pd
from database import semua_transaksi

def buat_excel():

    data = semua_transaksi()

    df = pd.DataFrame(
        data,
        columns=[
            "Tanggal",
            "Tipe",
            "Kategori",
            "Nominal",
            "Keterangan"
        ]
    )

    nama_file = "rekap_keuangan.xlsx"

    df.to_excel(
        nama_file,
        index=False
    )

    return nama_file