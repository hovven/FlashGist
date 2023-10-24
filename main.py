from bots import telegram_bot
from utils.helpers import setup_logging
from dotenv import load_dotenv

load_dotenv()
logger = setup_logging()

if __name__ == "__main__":
    logger.info("Starting the Telegram bot.")
    telegram_bot.app.run()
