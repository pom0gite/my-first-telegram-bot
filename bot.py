import json
import logging
import os
import random
from dataclasses import dataclass
from pathlib import Path

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


BASE_DIR = Path(__file__).resolve().parent
CONTENT_DIR = BASE_DIR / "content"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("pref-bot")

@dataclass(frozen=True)
class Item:
    id: str
    title: str
    text: str


def load_items(filename: str) -> list[Item]:
    path = CONTENT_DIR / filename
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [Item(id=str(x["id"]), title=str(x["title"]), text=str(x["text"])) for x in raw]


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Уроки", callback_data="lessons:list")],
            [InlineKeyboardButton("Ситуации (разбор)", callback_data="situations:list")],
            [
                InlineKeyboardButton("Случайная ситуация", callback_data="situations:random"),
                InlineKeyboardButton("Мини-квиз", callback_data="quiz:start"),
            ],
            [InlineKeyboardButton("Помощь", callback_data="help")],
        ]
    )

