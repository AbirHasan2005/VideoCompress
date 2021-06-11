#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K / Akshay C / @AbirHasan2005

# the logging things

import datetime
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

from bot.database import Database
import os, time, json
from bot.localisation import Localisation
from bot import (
    DOWNLOAD_LOCATION,
    AUTH_USERS,
    LOG_CHANNEL,
    UPDATES_CHANNEL,
    DATABASE_URL,
    SESSION_NAME
)
from bot.helper_funcs.ffmpeg import (
    convert_video,
    media_info,
    take_screen_shot
)
from bot.helper_funcs.display_progress import (
    progress_for_pyrogram,
    TimeFormatter
)
from bot.helper_funcs.compress import _compress

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

from bot.helper_funcs.utils import (
    delete_downloads
)

db = Database(DATABASE_URL, SESSION_NAME)
broadcast_ids = {}


async def incoming_start_message_f(bot, update):
    """/start command"""
    if not await db.is_user_exist(update.chat.id):
        await db.add_user(update.chat.id)
    if UPDATES_CHANNEL is not None:
        message = update
        client = bot
        try:
            user = await client.get_chat_member(UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await message.reply_text(
                    text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await message.reply_text(
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Join Updates Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await message.reply_text(
                text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    await bot.send_message(
        chat_id=update.chat.id,
        text=Localisation.START_TEXT,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Updates Channel', url='https://t.me/Discovery_Updates')
                ],
                [
                    InlineKeyboardButton('Support Group', url='https://t.me/linux_repo')
                ]
            ]
        ),
        reply_to_message_id=update.message_id,
    )


async def incoming_compress_message_f(bot, update):
    """/compress command"""
    if not await db.is_user_exist(update.chat.id):
        await db.add_user(update.chat.id)
    if UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(UPDATES_CHANNEL, update.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=update.chat.id,
                    text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=update.chat.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Join Updates Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=update.chat.id,
                text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if update.reply_to_message is None:
        try:
            await bot.send_message(
                chat_id=update.chat.id,
                text="🤬 Reply to telegram media 🤬",
                reply_to_message_id=update.message_id
            )
        except:
            pass
        return
    target_percentage = 50
    isAuto = False
    if len(update.command) > 1:
        try:
            if (int(update.command[1]) <= 90) and (int(update.command[1]) >= 10):
                target_percentage = int(update.command[1])
            else:
                try:
                    await bot.send_message(
                        chat_id=update.chat.id,
                        text="🤬 Value should be 10 to 90",
                        reply_to_message_id=update.message_id
                    )
                    return
                except:
                    pass
        except:
            pass
    else:
        isAuto = True
    _compress(bot, update, isAuto, target_percentage)

async def incoming_cancel_message_f(bot, update):
    """/cancel command"""
    if update.from_user.id not in AUTH_USERS:
        try:
            await update.message.delete()
        except:
            pass
        return

    status = DOWNLOAD_LOCATION + "/status.json"
    if os.path.exists(status):
        inline_keyboard = []
        ikeyboard = []
        ikeyboard.append(InlineKeyboardButton("Yes 🚫", callback_data=("fuckingdo").encode("UTF-8")))
        ikeyboard.append(InlineKeyboardButton("No 🤗", callback_data=("fuckoff").encode("UTF-8")))
        inline_keyboard.append(ikeyboard)
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.reply_text("Are you sure? 🚫 This will stop the compression!", reply_markup=reply_markup,
                                quote=True)
    else:
        delete_downloads()
        await bot.send_message(
            chat_id=update.chat.id,
            text="No active compression exists",
            reply_to_message_id=update.message_id
        )


async def incoming_video_f(bot, update: Message):
    if not await db.is_user_exist(update.chat.id):
        await db.add_user(update.chat.id)
    if UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(UPDATES_CHANNEL, update.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=update.chat.id,
                    text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=update.chat.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Join Updates Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=update.chat.id,
                text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    media = update.video or update.document
    if (media is None) or (media.file_name.rsplit(".", 1)[-1].startswith("mkv") is False) or (media.file_name.rsplit(".", 1)[-1].startswith("mp4") is False):
        try:
            await bot.send_message(
                chat_id=update.chat.id,
                text="Send Any MKV or MP4 Video Unkil!",
                reply_to_message_id=update.message_id
            )
        except:
            pass
        return
    # The Fu*king Logic
    markup = [[], [], [], [], []]
    for i in range(5, 21, 5):
        markup[0].append(InlineKeyboardButton(f"{str(i)}%", callback_data=f"compress_{str(i)}"))
    for i in range(25, 41, 5):
        markup[1].append(InlineKeyboardButton(f"{str(i)}%", callback_data=f"compress_{str(i)}"))
    for i in range(45, 61, 5):
        markup[2].append(InlineKeyboardButton(f"{str(i)}%", callback_data=f"compress_{str(i)}"))
    for i in range(65, 81, 5):
        markup[3].append(InlineKeyboardButton(f"{str(i)}%", callback_data=f"compress_{str(i)}"))
    for i in range(85, 96, 5):
        markup[4].append(InlineKeyboardButton(f"{str(i)}%", callback_data=f"compress_{str(i)}"))
    markup.append([InlineKeyboardButton("Close", callback_data="closeMeh")])
    await update.reply_text(
        text="Choose Compress Level from below buttons:",
        reply_markup=InlineKeyboardMarkup(markup),
        quote=True
    )
