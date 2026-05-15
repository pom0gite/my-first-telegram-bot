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

def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("← В меню", callback_data="menu")]])


def list_keyboard(prefix: str, items: list[Item]) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for it in items:
        rows.append([InlineKeyboardButton(it.title, callback_data=f"{prefix}:open:{it.id}")])
    rows.append([InlineKeyboardButton("← В меню", callback_data="menu")])
    return InlineKeyboardMarkup(rows)


def esc_md(text: str) -> str:
    for ch in ("_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"):
        text = text.replace(ch, f"\\{ch}")
    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "Привет! Я бот для обучения игре в преферанс.\nВыбирай раздел ниже.",
            reply_markup=main_menu(),
        )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "/start - запуск\n/menu - меню\n\nИспользуй кнопки для уроков и разбора ситуаций.",
            reply_markup=main_menu(),
        )


async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Меню.", reply_markup=main_menu())


async def text_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Для навигации используй кнопки.", reply_markup=main_menu())


async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return



