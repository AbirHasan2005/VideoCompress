#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | @AbirHasan2005

# the logging things

from bot.helper_funcs.utils import(
    delete_downloads
)
import logging
import os
import json
import shutil
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger(__name__)

from pyrogram.types import CallbackQuery
#from bot.helper_funcs.admin_check import AdminCheck
from bot import (
    AUTH_USERS,
    DOWNLOAD_LOCATION
)

async def button(bot, update: CallbackQuery):
    cb_data = update.data
    try:
        g = await AdminCheck(bot, update.message.chat.id, update.from_user.id)
        print(g)
    except:
        pass
    LOGGER.info(update.message.reply_to_message.from_user.id)
    if (update.from_user.id == update.message.reply_to_message.from_user.id) or g:
        print(cb_data)
        if cb_data == "fuckingdo":
            if update.from_user.id in AUTH_USERS:
                status = DOWNLOAD_LOCATION + "/status.json"
                with open(status, 'r+') as f:
                    statusMsg = json.load(f)
                    statusMsg['running'] = False
                    f.seek(0)
                    json.dump(statusMsg, f, indent=2)
                    if 'pid' in statusMsg.keys():
                        try:
                            os.kill(statusMsg["pid"], 9)
                        except:
                            pass
                        delete_downloads()
                    try:
                        await bot.delete_messages(update.message.chat.id, statusMsg["message"])
                    except:
                        pass
                    try:
                        await update.message.edit_text("🚦🚦 Last Process Stopped 🚦🚦")
                    except:
                        pass
            else:
                try:
                    await update.message.edit_text("You are not allowed to do that 🤭")
                except:
                    pass
        elif cb_data == "fuckoff":
            try:
                await update.message.edit_text("Okay! Fine 🤬")
            except:
                pass
				
