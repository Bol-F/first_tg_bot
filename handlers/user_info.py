import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils.db import db

logger = logging.getLogger(__name__)


async def info_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    uid = user.id

    # Пытаемся вытащить профиль из БД
    profile = db.get_user_profile(uid)
    if profile:
        profile_text = (
            f"👤 <b>Имя:</b> {profile['first_name']}\n"
            f"👥 <b>Фамилия:</b> {profile['last_name']}\n"
            f"🎂 <b>Возраст:</b> {profile['age']}\n"
            f"🏙️ <b>Город:</b> {profile['city']}\n"
            f"⏱️ <b>Обновлён:</b> {profile['updated_at']}\n\n"
        )
    else:
        profile_text = "<i>No saved profile found. Use /anketa to fill it.</i>\n\n"

    # Базовая инфа
    info = (
        profile_text + f"<b>Telegram ID:</b> <code>{uid}</code>\n"
        f"<b>Chat type:</b> {chat.type}\n"
        f"<b>Language:</b> {user.language_code or '—'}"
    )

    await update.message.reply_text(info, parse_mode="HTML")
    logger.info(f"Info sent to user {uid}")
