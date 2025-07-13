import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes,
)
from utils.db import Database

logger = logging.getLogger(__name__)

# Initialize database
db = Database()

# Conversation states
(
    STEP_NAME,
    STEP_SURNAME,
    STEP_AGE,
    STEP_CITY,
    STEP_DOB_DAY,
    STEP_DOB_MONTH,
    STEP_DOB_YEAR,
    STEP_PHONE,
    ASK_QUESTION,
    MORE_QUESTIONS,
) = range(10)


async def anketa_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the survey conversation, or continue if already completed."""
    user = update.effective_user
    profile = db.get_user_profile(user.id)

    if profile:
        await update.message.reply_text(
            "📋 Вы уже заполнили анкету. Теперь можете задать вопрос.\n\nНапишите ваш вопрос:"
        )
        return ASK_QUESTION

    await update.message.reply_text(
        f"📝 Привет, {user.first_name}! Давайте заполним анкету.\n\nВведите ваше имя:"
    )
    return STEP_NAME


async def anketa_step_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if not name or len(name) < 2:
        await update.message.reply_text(
            "❌ Имя должно содержать минимум 2 символа. Попробуйте еще раз:"
        )
        return STEP_NAME

    context.user_data["name"] = name
    await update.message.reply_text("Теперь введите вашу фамилию:")
    return STEP_SURNAME


async def anketa_step_surname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    surname = update.message.text.strip()
    if not surname or len(surname) < 2:
        await update.message.reply_text(
            "❌ Фамилия должна содержать минимум 2 символа. Попробуйте еще раз:"
        )
        return STEP_SURNAME

    context.user_data["surname"] = surname
    await update.message.reply_text("Введите ваш возраст:")
    return STEP_AGE


async def anketa_step_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age_text = update.message.text.strip()
    try:
        age = int(age_text)
        if age < 1 or age > 120:
            await update.message.reply_text(
                "❌ Возраст должен быть от 1 до 120 лет. Попробуйте еще раз:"
            )
            return STEP_AGE
    except ValueError:
        await update.message.reply_text(
            "❌ Пожалуйста, введите возраст числом. Попробуйте еще раз:"
        )
        return STEP_AGE

    context.user_data["age"] = age
    await update.message.reply_text("Теперь введите ваш город:")
    return STEP_CITY


async def anketa_step_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()
    if not city or len(city) < 2:
        await update.message.reply_text(
            "❌ Название города должно содержать минимум 2 символа. Попробуйте еще раз:"
        )
        return STEP_CITY

    context.user_data["city"] = city
    await update.message.reply_text(
        "Теперь введите день рождения (только число от 1 до 31):"
    )
    return STEP_DOB_DAY


async def anketa_step_dob_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day_text = update.message.text.strip()
    try:
        day = int(day_text)
        if day < 1 or day > 31:
            await update.message.reply_text(
                "❌ День должен быть от 1 до 31. Попробуйте еще раз:"
            )
            return STEP_DOB_DAY
    except ValueError:
        await update.message.reply_text(
            "❌ Пожалуйста, введите день числом. Попробуйте еще раз:"
        )
        return STEP_DOB_DAY

    context.user_data["dob_day"] = day
    await update.message.reply_text("Теперь введите месяц рождения (число от 1 до 12):")
    return STEP_DOB_MONTH


async def anketa_step_dob_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    month_text = update.message.text.strip()
    try:
        month = int(month_text)
        if month < 1 or month > 12:
            await update.message.reply_text(
                "❌ Месяц должен быть от 1 до 12. Попробуйте еще раз:"
            )
            return STEP_DOB_MONTH
    except ValueError:
        await update.message.reply_text(
            "❌ Пожалуйста, введите месяц числом. Попробуйте еще раз:"
        )
        return STEP_DOB_MONTH

    context.user_data["dob_month"] = month
    await update.message.reply_text("Теперь введите год рождения (например, 1990):")
    return STEP_DOB_YEAR


from datetime import date


async def anketa_step_dob_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    year_text = update.message.text.strip()
    try:
        year = int(year_text)
        if year < 1900 or year > date.today().year:
            await update.message.reply_text(
                f"❌ Год должен быть от 1900 до {date.today().year}. Попробуйте еще раз:"
            )
            return STEP_DOB_YEAR
    except ValueError:
        await update.message.reply_text(
            "❌ Пожалуйста, введите год числом. Попробуйте еще раз:"
        )
        return STEP_DOB_YEAR

    day = context.user_data["dob_day"]
    month = context.user_data["dob_month"]

    # Проверка корректности даты
    try:
        dob = date(year, month, day)
    except ValueError:
        await update.message.reply_text(
            "❌ Некорректная дата рождения. Проверьте день, месяц и год. Введите год снова:"
        )
        return STEP_DOB_YEAR

    # Проверка соответствия возраста дате рождения
    today = date.today()
    real_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    age_entered = context.user_data["age"]

    if real_age != age_entered:
        await update.message.reply_text(
            f"❌ Введённый возраст ({age_entered}) не совпадает с датой рождения "
            f"({dob.strftime('%d.%m.%Y')}). Вам должно быть {real_age} лет.\n\n"
            f"Проверьте и введите год заново:"
        )
        return STEP_DOB_YEAR

    context.user_data["dob_year"] = year

    await update.message.reply_text(
        "📱 Теперь введите ваш номер телефона после 998 (только цифры, без пробелов):\n\n"
        "Например: 901234567"
    )
    return STEP_PHONE


async def anketa_step_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_text = update.message.text.strip()

    # Check if it's only digits
    if not phone_text.isdigit():
        await update.message.reply_text(
            "❌ Номер телефона должен содержать только цифры, без пробелов и других символов. Попробуйте еще раз:"
        )
        return STEP_PHONE

    # Check length (should be 9 digits for Uzbekistan after 998)
    if len(phone_text) != 9:
        await update.message.reply_text(
            "❌ Номер телефона должен содержать 9 цифр после 998. Попробуйте еще раз:"
        )
        return STEP_PHONE

    # Check if it starts with valid operator codes
    valid_prefixes = ["90", "91", "93", "94", "95", "97", "98", "99"]
    if not any(phone_text.startswith(prefix) for prefix in valid_prefixes):
        await update.message.reply_text(
            "❌ Номер телефона должен начинаться с кода оператора (90, 91, 93, 94, 95, 97, 98, 99). Попробуйте еще раз:"
        )
        return STEP_PHONE

    full_phone = "998" + phone_text
    context.user_data["phone"] = full_phone

    # Save all data to database
    user = update.effective_user
    name = context.user_data.get("name")
    surname = context.user_data.get("surname")
    age = context.user_data.get("age")
    city = context.user_data.get("city")
    dob_day = context.user_data.get("dob_day")
    dob_month = context.user_data.get("dob_month")
    dob_year = context.user_data.get("dob_year")
    phone = context.user_data.get("phone")

    # Format date of birth
    date_of_birth = f"{dob_day:02d}.{dob_month:02d}.{dob_year}"

    # Save to DB
    db.save_user_profile(user.id, name, surname, age, city, date_of_birth, phone)

    await update.message.reply_text(
        f"✅ Анкета успешно заполнена!\n\n"
        f"👤 Имя: {name} {surname}\n"
        f"🎂 Возраст: {age}\n"
        f"📅 Дата рождения: {date_of_birth}\n"
        f"🏙️ Город: {city}\n"
        f"📱 Телефон: +{phone}\n\n"
        f"Теперь напишите свой вопрос:"
    )
    return ASK_QUESTION


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["question"] = update.message.text

    keyboard = ReplyKeyboardMarkup(
        [["➕ Ещё вопросы", "❌ Больше нет"]], resize_keyboard=True
    )

    await update.message.reply_text("Хотите задать ещё вопрос?", reply_markup=keyboard)
    return MORE_QUESTIONS


async def more_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text
    if answer == "➕ Ещё вопросы":
        await update.message.reply_text(
            "Пожалуйста, напишите ещё один вопрос:", reply_markup=ReplyKeyboardRemove()
        )
        return ASK_QUESTION
    else:
        await update.message.reply_text(
            "✅ Спасибо! Мы скоро ответим на ваши вопросы.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END


async def anketa_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Анкета отменена.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def register_conversation_handler(app):
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("anketa", anketa_start)],
        states={
            STEP_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, anketa_step_name)
            ],
            STEP_SURNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, anketa_step_surname)
            ],
            STEP_AGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, anketa_step_age)
            ],
            STEP_CITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, anketa_step_city)
            ],
            STEP_DOB_DAY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, anketa_step_dob_day)
            ],
            STEP_DOB_MONTH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, anketa_step_dob_month)
            ],
            STEP_DOB_YEAR: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, anketa_step_dob_year)
            ],
            STEP_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, anketa_step_phone)
            ],
            ASK_QUESTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_question)
            ],
            MORE_QUESTIONS: [
                MessageHandler(
                    filters.Regex("^(➕ Ещё вопросы|❌ Больше нет)$"), more_questions
                )
            ],
        },
        fallbacks=[CommandHandler("cancel", anketa_cancel)],
    )
    app.add_handler(conv_handler)
    logger.info("Conversation handler with questions registered")
