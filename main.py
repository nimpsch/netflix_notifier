import asyncio
import os
import time

from config.settings import ProviderFactory, ProviderName
from core.provider_handler import ProviderHandler
from telegram_bot import send, error_msg


def main():
    try:
        ProviderFactory.load_providers()
        gmx_provider = ProviderFactory.get_provider(ProviderName.GMX)
        handler = ProviderHandler(gmx_provider)
        # uid_list = handler.fetch_newsletter_uids()
        # handler.move(uid_list, destination_folder="Newsletter")
        # handler.click_on_newsletter()
        print("Checking mails!")
        results = handler.fetch_new_mails("Netflix")
        for result in results:
            asyncio.run(send(result.html, token=os.environ["TELEGRAM_BOT_TOKEN"], chat_id=os.environ["TELEGRAM_CHAT_ID"]))
        else:
            print("No new mails found.")
    except Exception as e:
        print(f"Error: {e}")
        # asyncio.run(error_msg(str(e), token=os.environ["TELEGRAM_BOT_TOKEN"], chat_id=os.environ["TELEGRAM_CHAT_ID"]))
    sleep_time = 30
    try:
        sleep_time = int(os.environ.get("SLEEP_TIME", 30))
    except (ValueError, Exception):
        pass
    print(f"Waiting {sleep_time} seconds")
    time.sleep(sleep_time)
    print("Done!")


if __name__ == "__main__":
    main()
