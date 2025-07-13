import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from telegram.error import TelegramError

# Import utilities
from utils.config import Config
from utils.logger import setup_logger

# Import handlers
from handlers.basic import start_cmd, help_cmd, status_cmd, echo_msg
from handlers.user_info import info_cmd
from handlers.buttons import menu_cmd, button_callback
from handlers.conversation import register_conversation_handler


async def error_handler(update, context):
    """Handle errors"""
    logger = logging.getLogger(__name__)
    logger.error(f"Update {update} caused error {context.error}")

    if update and update.effective_message:
        await update.effective_message.reply_text(
            "🚨 Произошла ошибка. Попробуйте еще раз или обратитесь к администратору."
        )


def main():
    """Main function to start the bot"""
    # Setup
    Config.validate()
    logger = setup_logger()

    try:
        # Create application
        app = ApplicationBuilder().token(Config.TOKEN).build()

        # Register handlers
        app.add_handler(CommandHandler("start", start_cmd))
        app.add_handler(CommandHandler("help", help_cmd))
        app.add_handler(CommandHandler("status", status_cmd))
        app.add_handler(CommandHandler("info", info_cmd))
        app.add_handler(CommandHandler("menu", menu_cmd))
        app.add_handler(CallbackQueryHandler(button_callback))

        # Register conversation handler
        register_conversation_handler(app)

        # Echo handler (should be last)
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_msg))

        # Error handler
        app.add_error_handler(error_handler)

        logger.info("🚀 Bot started successfully!")
        logger.info(f"Debug mode: {Config.DEBUG}")

        # Start polling
        app.run_polling(drop_pending_updates=True)

    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()
