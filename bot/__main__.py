#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | @AbirHasan2005


import os

from bot import (
    APP_ID,
    API_HASH,
    AUTH_USERS,
    DOWNLOAD_LOCATION,
    LOGGER,
    TG_BOT_TOKEN,
    BOT_USERNAME
)
from bot.plugins.new_join_fn import (	
    help_message_f	
)

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from bot.plugins.incoming_message_fn import (
    incoming_start_message_f,
    incoming_compress_message_f,
    incoming_cancel_message_f
)

from bot.plugins.status_message_fn import (
    exec_message_f,
    upload_log_file
)

from bot.commands import Command
from bot.plugins.call_back_button_handler import button

if __name__ == "__main__" :
    # create download directory, if not exist
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    #
    sessions = "/app/sessions"
    if not os.path.isdir(sessions):
        os.makedirs(sessions)
    app = Client(
        "SGVideoCompressBot",
        bot_token=TG_BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        workers=2
    )
    #
    app.set_parse_mode("html")
    #
    # START command
    incoming_start_message_handler = MessageHandler(
        incoming_start_message_f,
        filters=filters.command(["start", f"start@{BOT_USERNAME}"])
    )
    app.add_handler(incoming_start_message_handler)
    
    # COMPRESS command
    incoming_compress_message_handler = MessageHandler(
        incoming_compress_message_f,
        filters=filters.command(["compress", f"compress@{BOT_USERNAME}"])
    )
    app.add_handler(incoming_compress_message_handler)
    
    # CANCEL command
    incoming_cancel_message_handler = MessageHandler(
        incoming_cancel_message_f,
        filters=filters.command(["cancel", f"cancel@{BOT_USERNAME}"]) & filters.chat(chats=AUTH_USERS)
    )
    app.add_handler(incoming_cancel_message_handler)

    # MEMEs COMMANDs
    exec_message_handler = MessageHandler(
        exec_message_f,
        filters=filters.command(["exec", f"exec@{BOT_USERNAME}"]) & filters.chat(chats=AUTH_USERS)
    )
    app.add_handler(exec_message_handler)
    
    # HELP command
    help_text_handler = MessageHandler(
        help_message_f,
        filters=filters.command(["help", f"help@{BOT_USERNAME}"])
    )
    app.add_handler(help_text_handler)
    
    # Telegram command to upload LOG files
    upload_log_f_handler = MessageHandler(
        upload_log_file,
        filters=filters.command(["log", f"log@{BOT_USERNAME}"]) & filters.chat(chats=AUTH_USERS)
    )
    app.add_handler(upload_log_f_handler)
    
    call_back_button_handler = CallbackQueryHandler(
        button
    )
    app.add_handler(call_back_button_handler)

    # run the APPlication
    app.run()
