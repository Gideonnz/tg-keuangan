import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("USER_ID"))
client = TelegramClient(
    "tgbot",
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
    ).start(bot_token=TOKEN
)


def main():
    buat_database()
    print("Bot Bekerja Dengan Baik.")

    client.start()
    client.run_until_disconnected()



if __name__=="__main__":
    main()
