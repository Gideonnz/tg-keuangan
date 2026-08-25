import json
from google import genai
from google.genai import types
from Finance import GEMINI_API_KEY as GEMINI_KEY

client = genai.Client(api_key=GEMINI_KEY)

def baca_transaksi_gambar(path):
    with open(path, "rb") as f:
        image_bytes = f.read()

    image = types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/jpeg",
    )

    prompt = """
Anda adalah AI pencatat keuangan.

Analisa gambar bukti transaksi.

Kembalikan JSON saja:

{
 "tipe": "MASUK atau KELUAR",
 "nominal": angka,
 "kategori": "kategori transaksi",
 "keterangan": "deskripsi singkat"
}

Jika tidak yakin, lakukan perkiraan terbaik.
"""

    config = types.GenerateContentConfig(
        response_mime_type="application/json"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, image],
        config=config
    )

    return json.loads(response.text)
