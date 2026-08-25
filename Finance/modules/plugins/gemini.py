import json
import google.generativeai as genai
from Finance import GEMINI_API_KEY as GEMINI_KEY


genai.configure(
  api_key=GEMINI_KEY
)


model = genai.GenerativeModel(
    "gemini-1.5-flash"
)



def baca_transaksi_gambar(path):

    image = {
        "mime_type": "image/jpeg",
        "data": open(
            path,
            "rb"
        ).read()
    }


    prompt = """
Anda adalah AI pencatat keuangan.

Analisa gambar bukti transaksi.

Kembalikan JSON saja:

{
 "tipe":"MASUK atau KELUAR",
 "nominal":angka,
 "kategori":"kategori transaksi",
 "keterangan":"deskripsi singkat"
}

Jika tidak yakin, lakukan perkiraan terbaik.
Jangan tambahkan teks lain.
"""


    response = model.generate_content(
        [
            prompt,
            image
        ]
    )


    hasil = response.text


    hasil = hasil.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    )


    return json.loads(hasil)
