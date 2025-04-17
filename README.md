# 🎂 Birthday Countdown Bot

Этот бот каждый день отправляет сообщение в канал или чат, сколько дней осталось до твоего дня рождения. А за час до наступления праздника напоминает, что пора отмечать 🎉

## 📦 Установка

1. Склонируй репозиторий:
```bash
git clone https://github.com/xelvorn/birthday-bot.git
cd birthday-bot
```
2. Установи зависимости:
```bash
pip install -r requirements.txt
```
3. Отредактируй config.py и вставь свой токен, ID чата и дату рождения.
4. Запусти бота:
```bash
python bot.py
```

## 🐳 Использование с Docker
1. Собери образ:
```bash
docker build -t birthday-bot .
```
2. Запусти контейнер:
```bash
docker run -d --name my_birthday_bot birthday-bot
```
## 🔧 Настройки

Все настройки находятся в `config.py`:

- `BOT_TOKEN` — токен Telegram-бота
- `CHANNEL_ID` — ID чата или канала
- `BIRTHDAY_MONTH` и `BIRTHDAY_DAY` — дата твоего рождения

## 💬 Пример сообщений

- "Осталась неделя до моего дня рождения! Готовьте подарки 🎁"
- "До моего дня рождения осталось 3 дня!"
- "До моего дня рождения остался 1 час!!! Скоро праздник 🎂"

## 📜 Лицензия
MIT License
