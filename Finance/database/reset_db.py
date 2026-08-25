from . import koneksi

def reset_database():

    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM transaksi
    """)

    cursor.execute("""
    DELETE FROM pengaturan
    """)

    cursor.execute("""
    DELETE FROM sqlite_sequence
    WHERE name='transaksi'
    """)

    conn.commit()
    conn.close()
