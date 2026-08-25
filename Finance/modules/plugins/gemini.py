import json
import logging
from google import genai
from google.genai import types
from google.genai.errors import APIError
from Finance import GEMINI_API_KEY as GEMINI_KEY

client = genai.Client(api_key=GEMINI_KEY)

def baca_transaksi_gambar(path):
    try:
        with open(path, "rb") as f:
            image_bytes = f.read()

        image = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/jpeg",
        )

        prompt = """
Anda adalah AI pencatat keuangan.
Analisa gambar bukti transaksi.

Kembalikan JSON saja dengan struktur:
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

    except FileNotFoundError:
        logging.error(f"File gambar tidak ditemukan pada path: {path}")
        return {"error": "File gambar tidak ditemukan"}

    except APIError as e:
        logging.error(f"Error dari Gemini API: {e}")
        return {"error": "Gagal menghubungi API Gemini"}

    except json.JSONDecodeError:
        logging.error("Respons dari Gemini bukan merupakan JSON yang valid.")
        try:
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception:
            return {"error": "Gagal membaca format data transaksi"}

    except Exception as e:
        logging.error(f"Terjadi kesalahan yang tidak terduga: {e}")
        return {"error": "Terjadi kesalahan sistem"}
