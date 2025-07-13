import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /menu command"""
    try:
        keyboard = [
            [InlineKeyboardButton("🎯 Опция 1", callback_data="option_1")],
            [InlineKeyboardButton("🎨 Опция 2", callback_data="option_2")],
            [InlineKeyboardButton("🎪 Опция 3", callback_data="option_3")],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
            [InlineKeyboardButton("❌ Закрыть", callback_data="close")],
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🎛️ <b>Интерактивное меню:</b>\n\nВыберите опцию:",
            reply_markup=markup,
            parse_mode="HTML",
        )
        logger.info(f"Menu shown to user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error in menu_cmd: {e}")
        await update.message.reply_text("Ошибка при показе меню.")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    try:
        query = update.callback_query
        await query.answer()

        user = update.effective_user
        data = query.data

        responses = {
            "option_1": "🎯 Вы выбрали первую опцию! Отличный выбор!",
            "option_2": "🎨 Вы выбрали вторую опцию! Креативно!",
            "option_3": "🎪 Вы выбрали третью опцию! Интересно!",
            "stats": f"📊 Статистика:\n👤 Пользователь: {user.first_name}\n🆔 ID: {user.id}",
            "close": "❌ Меню закрыто.",
        }

        response = responses.get(data, f"Неизвестная опция: {data}")
        await query.edit_message_text(response)
        logger.info(f"User {user.id} pressed button: {data}")
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")
