import glob
import logging
from pathlib import Path
from Finance import client
from Finance.utils import load_plugins
from Finance.database import buat_database

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

path = "Finance/modules/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))

def main():
    buat_database()
    print("Bot Bekerja Dengan Baik.")

    client.start()
    client.run_until_disconnected()


if __name__=="__main__":
    main()
