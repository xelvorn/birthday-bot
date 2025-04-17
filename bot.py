import logging
from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN, CHANNEL_ID, BIRTHDAY_MONTH, BIRTHDAY_DAY

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

default_template = "До моего дня рождения {verb} {days} {word}! Готовьте подарки!"
hour_before_message = "До моего дня рождения остался 1 час!!! Скоро праздник 🎂"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def russian_plural(days: int) -> str:
    """
    Получает правильное окончание слова "день" в зависимости от количества
    """
    if days % 10 == 1 and days % 100 != 11:
        return 'день'
    elif 2 <= days % 10 <= 4 and not (12 <= days % 100 <= 14):
        return 'дня'
    else:
        return 'дней'

async def send_countdown():
    """
    Отправляет ежедневное сообщение о том, сколько осталось до ДР
    """
    today = date.today()
    year = today.year if (today.month, today.day) <= (BIRTHDAY_MONTH, BIRTHDAY_DAY) else today.year + 1
    birthday = date(year, BIRTHDAY_MONTH, BIRTHDAY_DAY)
    days_left = (birthday - today).days

    if days_left in custom_messages:
        text = custom_messages[days_left]
    else:
        word = russian_plural(days_left)
        verb = 'остался' if days_left % 10 == 1 and days_left % 100 != 11 else 'осталось'
        text = default_template.format(verb=verb, days=days_left, word=word)

    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=text)
        logging.info(f"Sent countdown message: {text}")
    except Exception as e:
        logging.error(f"Failed to send countdown message: {e}")

async def send_hour_alert():
    """
    Отправляет сообщение за час до дня рождения
    """
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=hour_before_message)
        logging.info("Sent hour-before alert")
    except Exception as e:
        logging.error(f"Failed to send hour-before message: {e}")

async def on_startup(dp):
    """
    Запускается при старте бота
    """
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_countdown, CronTrigger(hour=3, minute=0), id="daily_countdown", replace_existing=True)
    scheduler.add_job(send_hour_alert, CronTrigger(month=BIRTHDAY_MONTH, day=BIRTHDAY_DAY, hour=23, minute=0), id="hour_before_alert", replace_existing=True)
    scheduler.start()
    logging.info("Scheduler started")

    # тестовый прогон
    await send_countdown()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
