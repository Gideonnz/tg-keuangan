import sqlite3

DB_NAME = "keuangan.db"

def koneksi():
  return sqlite3.connect(DB_NAME)
