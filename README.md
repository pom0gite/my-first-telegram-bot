# my-first-telegram-bot
pref-training 
# pref-bot

Telegram-бот для обучения игре в преферанс:
- короткие уроки;
- разбор игровых ситуаций;
- случайная ситуация;
- мини-квиз с объяснением логики.

## 1) Установка (Windows, PowerShell)

Перейди в папку проекта:

```powershell
cd "C:\Users\easym\OneDrive\Рабочий стол\bot\pref-bot"
```

Создай и активируй виртуальное окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Установи зависимости:

```powershell
pip install -r requirements.txt
```

## 2) Токен бота

1. Создай бота у [@BotFather](https://t.me/BotFather).
2. Скопируй токен и задай переменную окружения:

```powershell
$env:TELEGRAM_BOT_TOKEN="СЮДА_ТОКЕН"
```

## 3) Запуск

```powershell
python bot.py
```

Если всё ок, в консоли появится `Bot is running.`  
Дальше открой бота в Telegram и нажми `/start`.









