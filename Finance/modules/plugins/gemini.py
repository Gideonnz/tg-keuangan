import json
import logging
import mimetypes
from google import genai
from google.genai import types
from google.genai.errors import APIError
from Finance import GEMINI_API_KEY as GEMINI_KEY

client = genai.Client(api_key=GEMINI_KEY)

def baca_transaksi_dokumen(path):
    try:
        mime_type, _ = mimetypes.guess_type(path)
        if not mime_type:
            mime_type = "application/octet-stream"

        with open(path, "rb") as f:
            file_bytes = f.read()

        document_part = types.Part.from_bytes(
            data=file_bytes,
            mime_type=mime_type,
        )

        prompt = """
Anda adalah AI pencatat keuangan.
Analisis dokumen/file ini yang berisi satu atau BANYAK transaksi keuangan.

Kembalikan ARRAY/LIST JSON yang berisi seluruh transaksi yang terdeteksi dengan struktur setiap objek:
[
  {
   "tipe": "MASUK atau KELUAR",
   "nominal": angka,
   "kategori": "kategori transaksi",
   "keterangan": "deskripsi singkat"
  }
]

Jika hanya ada 1 transaksi, tetap kembalikan dalam bentuk list berisi 1 elemen.
"""

        config = types.GenerateContentConfig(
            response_mime_type="application/json"
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[prompt, document_part],
            config=config
        )

        hasil = json.loads(response.text)

        if isinstance(hasil, dict):
            if "error" in hasil:
                return hasil
            hasil = [hasil]

        return hasil

    except FileNotFoundError:
        logging.error(f"File dokumen tidak ditemukan pada path: {path}")
        return {"error": "File dokumen tidak ditemukan"}

    except APIError as e:
        logging.error(f"Error dari Gemini API: {e}")
        return {"error": "Gagal menghubungi API Gemini"}

    except json.JSONDecodeError:
        logging.error("Respons dari Gemini bukan merupakan JSON yang valid.")
        try:
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            hasil = json.loads(clean_text)
            if isinstance(hasil, dict):
                hasil = [hasil]
            return hasil
        except Exception:
            return {"error": "Gagal membaca format data transaksi"}

    except Exception as e:
        logging.error(f"Terjadi kesalahan yang tidak terduga: {e}")
        return {"error": "Terjadi kesalahan sistem"}
