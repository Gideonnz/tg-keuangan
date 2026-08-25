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

    conn.commit()
    conn.close()
