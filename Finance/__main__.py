import logging
from Finance import client
from Finance.database import buat_database

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

def main():
    buat_database()
    print("Bot Bekerja Dengan Baik.")

    client.start()
    client.run_until_disconnected()



if __name__=="__main__":
    main()
