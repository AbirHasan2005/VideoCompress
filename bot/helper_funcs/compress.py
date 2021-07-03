# (c) @AbirHasan2005 | @ballicipluck

from bot.database import Database
import os
import time
import json
import datetime
import logging
from bot.localisation import Localisation
from bot import (
    DOWNLOAD_LOCATION,
    LOG_CHANNEL,
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
from bot.helper_funcs.queue import (
    Queues
)
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from bot.helper_funcs.utils import (
    delete_downloads
)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
db = Database(DATABASE_URL, SESSION_NAME)
broadcast_ids = {}


async def _compress(bot: Client, update: Message, isAuto, target_percentage):
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
        download_start = await bot.send_message(LOG_CHANNEL,
                                                f"**Bot Become Busy Now !!** \n\nDownload Started at `{now}`",
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
                    ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime(
                        "%d/%m/%Y, %H:%M:%S")
                    bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime(
                        "%d/%m/%Y, %H:%M:%S")
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
        except ValueError as e:
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
                ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime(
                    "%d/%m/%Y, %H:%M:%S")
                bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime(
                    "%d/%m/%Y, %H:%M:%S")
                now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
                await bot.send_message(LOG_CHANNEL,
                                       f"**Download Failed, Bot is Free Now !!** \n\nProcess Done at `{now}`",
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
        compress_start = await bot.send_message(LOG_CHANNEL,
                                                f"**Compressing Video ...** \n\nProcess Started at `{now}`",
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
            upload_start = await bot.send_message(LOG_CHANNEL,
                                                  f"**Uploading Video ...** \n\nProcess Started at `{now}`",
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
            if upload is None:
                try:
                    await sent_message.edit_text(
                        text="Upload stopped"
                    )
                    ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime(
                        "%d/%m/%Y, %H:%M:%S")
                    bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime(
                        "%d/%m/%Y, %H:%M:%S")
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
                ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime(
                    "%d/%m/%Y, %H:%M:%S")
                bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime(
                    "%d/%m/%Y, %H:%M:%S")
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

    Queues.Q.pop(0)
    print('Updated Queue')
    Queues.IS_BUZY = False
    await Queues.check_queue()
