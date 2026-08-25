import pandas as pd
from telethon import events
from Finance import client
from Finance.status import user
from Finance.database.transaksi_db import semua_transaksi

def buat_excel(user_id):

    data = semua_transaksi(user_id)

    df = pd.DataFrame(
        data,
        columns=["ID", "Tanggal", "Tipe", "Kategori", "Nominal", "Keterangan"
        ]
    )

    nama_file = "rekap_keuangan.xlsx"

    df.to_excel(nama_file, index=False)

    return nama_file

@client.on(events.NewMessage(pattern="^[/.!]excel"))
async def excel(event):

    if not user(event):
        return

    file = buat_excel(event.sender_id)
    await client.send_file(
        event.chat_id,
        file,
        caption="Rekap Keuangan"
    )
