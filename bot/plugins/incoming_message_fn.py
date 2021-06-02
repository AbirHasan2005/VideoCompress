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
    user_file = str(update.from_user.id) + ".FFMpegRoBot.mkv"
    saved_file_path = DOWNLOAD_LOCATION + "/" + user_file
    LOGGER.info(saved_file_path)
    d_start = time.time()
    status = DOWNLOAD_LOCATION + "/status.json"
    if not os.path.exists(status):
        sent_message = await bot.send_message(
            chat_id=update.chat.id,
            text=Localisation.DOWNLOAD_START,
            reply_to_message_id=update.message_id
        )
        ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
        bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
        now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
        download_start = await bot.send_message(LOG_CHANNEL, f"**Bot Become Busy Now !!** \n\nDownload Started at `{now}`",
                                                parse_mode="markdown")
        try:
            d_start = time.time()
            status = DOWNLOAD_LOCATION + "/status.json"
            with open(status, 'w') as f:
                statusMsg = {
                    'running': True,
                    'message': sent_message.message_id
                }

                json.dump(statusMsg, f, indent=2)
            video = await bot.download_media(
                message=update.reply_to_message,
                file_name=saved_file_path,
                progress=progress_for_pyrogram,
                progress_args=(
                    bot,
                    Localisation.DOWNLOAD_START,
                    sent_message,
                    d_start
                )
            )
            LOGGER.info(video)
            if (video is None):
                try:
                    await sent_message.edit_text(
                        text="Download stopped"
                    )
                    ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
                    bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
                    now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
                    await bot.send_message(LOG_CHANNEL,
                                           f"**Download Stopped, Bot is Free Now !!** \n\nProcess Done at `{now}`",
                                           parse_mode="markdown")
                    await download_start.delete()
                except:
                    pass
                delete_downloads()
                LOGGER.info("Download stopped")
                return
        except (ValueError) as e:
            try:
                await sent_message.edit_text(
                    text=str(e)
                )
            except:
                pass
            delete_downloads()
        try:
            await sent_message.edit_text(
                text=Localisation.SAVED_RECVD_DOC_FILE
            )
        except:
            pass
    else:
        try:
            await bot.send_message(
                chat_id=update.chat.id,
                text=Localisation.FF_MPEG_RO_BOT_STOR_AGE_ALREADY_EXISTS,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Show Bot Status', url=f'https://t.me/{LOG_CHANNEL}')
                            # That's Username na ...
                        ]
                    ]
                ),
                reply_to_message_id=update.message_id
            )
        except:
            pass
        return

    if os.path.exists(saved_file_path):
        downloaded_time = TimeFormatter((time.time() - d_start) * 1000)
        duration, bitrate = await media_info(saved_file_path)
        if duration is None or bitrate is None:
            try:
                await sent_message.edit_text(
                    text="⚠️ Getting video meta data failed ⚠️"
                )
                ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
                bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
                now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
                await bot.send_message(LOG_CHANNEL, f"**Download Failed, Bot is Free Now !!** \n\nProcess Done at `{now}`",
                                       parse_mode="markdown")
                await download_start.delete()
            except:
                pass
            delete_downloads()
            return
        thumb_image_path = await take_screen_shot(
            saved_file_path,
            os.path.dirname(os.path.abspath(saved_file_path)),
            (duration / 2)
        )
        ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
        bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
        now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
        await download_start.delete()
        compress_start = await bot.send_message(LOG_CHANNEL, f"**Compressing Video ...** \n\nProcess Started at `{now}`",
                                                parse_mode="markdown")
        await sent_message.edit_text(
            text=Localisation.COMPRESS_START
        )
        c_start = time.time()
        o = await convert_video(
            saved_file_path,
            DOWNLOAD_LOCATION,
            duration,
            bot,
            sent_message,
            target_percentage,
            isAuto,
            compress_start
        )
        compressed_time = TimeFormatter((time.time() - c_start) * 1000)
        LOGGER.info(o)
        if o == 'stopped':
            return
        if o is not None:
            ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
            bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
            now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
            await compress_start.delete()
            upload_start = await bot.send_message(LOG_CHANNEL, f"**Uploading Video ...** \n\nProcess Started at `{now}`",
                                                  parse_mode="markdown")
            await sent_message.edit_text(
                text=Localisation.UPLOAD_START,
            )
            u_start = time.time()
            caption = Localisation.COMPRESS_SUCCESS.replace('{}', downloaded_time, 1).replace('{}', compressed_time, 1)
            upload = await bot.send_video(
                chat_id=update.chat.id,
                video=o,
                caption=caption,
                supports_streaming=True,
                duration=duration,
                thumb=thumb_image_path,
                reply_to_message_id=update.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    bot,
                    Localisation.UPLOAD_START,
                    sent_message,
                    u_start
                )
            )
            if (upload is None):
                try:
                    await sent_message.edit_text(
                        text="Upload stopped"
                    )
                    ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
                    bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
                    now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
                    await bot.send_message(LOG_CHANNEL,
                                           f"**Upload Stopped, Bot is Free Now !!** \n\nProcess Done at `{now}`",
                                           parse_mode="markdown")
                    await upload_start.delete()
                except:
                    pass
                delete_downloads()
                return
            uploaded_time = TimeFormatter((time.time() - u_start) * 1000)
            await sent_message.delete()
            delete_downloads()
            ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
            bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
            now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
            await upload_start.delete()
            await bot.send_message(LOG_CHANNEL, f"**Upload Done, Bot is Free Now !!** \n\nProcess Done at `{now}`",
                                   parse_mode="markdown")
            LOGGER.info(upload.caption)
            try:
                await upload.edit_caption(
                    caption=upload.caption.replace('{}', uploaded_time)
                )
            except:
                pass
        else:
            delete_downloads()
            try:
                await sent_message.edit_text(
                    text="⚠️ Compression failed ⚠️"
                )
                ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
                bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
                now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
                await bot.send_message(LOG_CHANNEL,
                                       f"**Compression Failed, Bot is Free Now !!** \n\nProcess Done at `{now}`",
                                       parse_mode="markdown")
                await download_start.delete()
            except:
                pass

    else:
        delete_downloads()
        try:
            await sent_message.edit_text(
                text="⚠️ Failed Downloaded path not exist ⚠️"
            )
            ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
            bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
            now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
            await bot.send_message(LOG_CHANNEL, f"**Download Error, Bot is Free Now !!** \n\nProcess Done at `{now}`",
                                   parse_mode="markdown")
            await download_start.delete()
        except:
            pass


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
