import logging
from datetime import datetime, date
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN, CHANNEL_ID, BIRTHDAY_MONTH, BIRTHDAY_DAY

# — инициализация Bot и Dispatcher для aiogram v2.25.2
bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(bot)

# логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# кастомные сообщения по количеству дней до ДР
custom_messages = {
    30: "остался месяц до моего др, уже можно задуматься над подарками",
    20: "20 дней до др, я вахуе как время летит",
    14: "до моего ДР две недели(14 дней), вы уже придумали чо мне дарить??",
    10: "10 дней до праздника",
    7:  "Осталась неделя до моего дня рождения! Готовьте подарки 🎁",
    5:  "Пять дней до моего ДР! пиздец время летит",
    3:  "Всего три дня до моего ДР! 🔥",
    2:  "Два дня и я уже старше на год",
    1:  "Завтра праздник! 🎈",
}

def russian_plural(days: int) -> str:
    """
    Правильное окончание слова "день"
    """
    if days % 10 == 1 and days % 100 != 11:
        return 'день'
    elif 2 <= days % 10 <= 4 and not (12 <= days % 100 <= 14):
        return 'дня'
    else:
        return 'дней'

def get_countdown_text() -> str:
    """
    Формирует текст отсчёта до ДР
    """
    today = datetime.now(ZoneInfo("Europe/Moscow")).date()
    year = today.year if (today.month, today.day) <= (BIRTHDAY_MONTH, BIRTHDAY_DAY) else today.year + 1
    birthday = date(year, BIRTHDAY_MONTH, BIRTHDAY_DAY)
    days_left = (birthday - today).days

    if days_left in custom_messages:
        return custom_messages[days_left]
    word = russian_plural(days_left)
    verb = 'остался' if days_left % 10 == 1 and days_left % 100 != 11 else 'осталось'
    return f"До моего дня рождения {verb} {days_left} {word}! Готовьте подарки!"

async def send_countdown():
    text = get_countdown_text()
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=text)
        logging.info(f"Sent countdown message: {text}")
    except Exception as e:
        logging.error(f"Failed to send countdown message: {e}")

async def send_hour_alert():
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text="До моего дня рождения остался 1 час!!! Скоро праздник 🎂")
        logging.info("Sent hour-before alert")
    except Exception as e:
        logging.error(f"Failed to send hour-before message: {e}")

async def on_startup(dp: Dispatcher):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # ежедневный отчёт в 00:00 МСК
    scheduler.add_job(
        send_countdown,
        CronTrigger(hour=0, minute=0, timezone=ZoneInfo("Europe/Moscow")),
        id="daily_countdown",
        replace_existing=True,
    )
    # оповещение за час до ДР
    scheduler.add_job(
        send_hour_alert,
        CronTrigger(month=BIRTHDAY_MONTH, day=BIRTHDAY_DAY, hour=23, minute=0, timezone=ZoneInfo("Europe/Moscow")),
        id="hour_before_alert",
        replace_existing=True,
    )
    scheduler.start()
    logging.info("Scheduler started")

    # тестовый единичный прогон: одно сообщение с отсчётом + заметка о недоступности в ЛС
    combined = f"{get_countdown_text()}\n\nБот не доступен в личных сообщениях. Исходники: https://github.com/xelvorn/birthday-bot"
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=combined)
        logging.info("Sent combined startup message")
    except Exception as e:
        logging.error(f"Failed to send startup message: {e}")

# Обработка личных сообщений
@dp.message_handler(lambda message: message.chat.type == 'private')
async def handle_private(message: types.Message):
    await message.reply(
        "Бот не доступен в личных сообщениях. Пожалуйста, используйте канал. "
        "Исходники: https://github.com/xelvorn/birthday-bot"
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
