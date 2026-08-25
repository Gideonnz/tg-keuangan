from . import koneksi


def reset_data():

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
    """)


    conn.commit()
    conn.close()
