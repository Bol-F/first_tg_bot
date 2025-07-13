import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    try:
        user = update.effective_user
        welcome_message = (
            f"👋 Привет, {user.first_name}!\n\n"
            "Я твой персональный бот-помощник. Вот что я умею:\n\n"
            "🔹 /help - Список всех команд\n"
            "🔹 /info - Твоя информация\n"
            "🔹 /anketa - Заполнить анкету\n"
            "🔹 /menu - Интерактивное меню\n"
            "🔹 /status - Статус бота\n\n"
            "Просто напиши мне что-нибудь, и я отвечу! 😊"
        )
        await update.message.reply_text(welcome_message)
        logger.info(f"User {user.id} ({user.first_name}) started the bot")
    except Exception as e:
        logger.error(f"Error in start_cmd: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуйте еще раз.")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    try:
        help_text = (
            "<b>📋 Список команд:</b>\n\n"
            "🚀 /start - Запустить бота\n"
            "ℹ️ /help - Показать это сообщение\n"
            "⚡ /status - Проверить статус бота\n"
            "👤 /info - Показать твою информацию\n"
            "📝 /anketa - Заполнить анкету\n"
            "🎛️ /menu - Интерактивное меню\n"
            "❌ /cancel - Отменить текущую операцию\n\n"
            "<i>Просто напиши мне сообщение, и я его повторю!</i>"
        )
        await update.message.reply_text(help_text, parse_mode="HTML")
        logger.info(f"Help requested by user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error in help_cmd: {e}")
        await update.message.reply_text("Ошибка при получении помощи.")


async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uptime_msg = (
            f"✅ <b>Статус бота:</b> Работаю отлично!\n"
            f"🕐 <b>Время:</b> {now}\n"
            f"🤖 <b>Версия:</b> 2.0\n"
            f"👤 <b>Пользователь:</b> {update.effective_user.first_name}"
        )
        await update.message.reply_text(uptime_msg, parse_mode="HTML")
        logger.info(f"Status requested by user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error in status_cmd: {e}")
        await update.message.reply_text("Ошибка при получении статуса.")


async def echo_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo user messages"""
    try:
        if not update.message or not update.message.text:
            return

        text = update.message.text
        user = update.effective_user

        # Add some variety to responses
        responses = [
            f"🔊 Ты написал: {text}",
            f"📝 Получил сообщение: {text}",
            f"💬 Ты сказал: {text}",
            f"🗣️ Твое сообщение: {text}",
        ]

        import random

        response = random.choice(responses)
        await update.message.reply_text(response)
        logger.info(f"Echo to {user.id} ({user.first_name}): {text}")
    except Exception as e:
        logger.error(f"Error in echo_msg: {e}")
