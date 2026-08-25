import pandas as pd
from telthon import events
from Finance import client
from Finance.status import user
from Finance.database.transaksi import semua_transaksi

def buat_excel():

    data = semua_transaksi()

    df = pd.DataFrame(
        data,
        columns=["Tanggal", "Tipe", "Kategori", "Nominal", "Keterangan"
        ]
    )

    nama_file = "rekap_keuangan.xlsx"

    df.to_excel(nama_file, index=False)

    return nama_file

@client.on(events.NewMessage(pattern="^[/.!]excel"))
async def excel(event):

    if not user(event):
        return

    file = buat_excel()
    await client.send_file(
        event.chat_id,
        file,
        caption="Rekap Keuangan"
    )
