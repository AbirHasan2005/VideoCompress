#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | @AbirHasan2005


from bot.localisation import Localisation
from bot import (
    UPDATES_CHANNEL
)
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

async def new_join_f(client, message):
    # delete all other messages, except for AUTH_USERS
    await message.delete(revoke=True)
    # reply the correct CHAT ID,
    # and LEAVE the chat
    chat_type = message.chat.type
    if chat_type != "private":
        await message.reply_text(
            Localisation.WRONG_MESSAGE.format(
                CHAT_ID=message.chat.id
            )
        )
        # leave chat
        await message.chat.leave()


async def help_message_f(client, message):
    ## Force Sub ##
    update_channel = UPDATES_CHANNEL
    if update_channel:
        try:
            user = await client.get_chat_member(update_channel, message.chat.id)
            if user.status == "kicked":
               await message.reply_text("Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).", parse_mode="markdown")
               return
        except UserNotParticipant:
            await message.reply_text(
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Join Updates Channel", url=f"https://t.me/{update_channel}")
                        ]
                    ]
                )
            )
            return
        except Exception:
            await message.reply_text("Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).", parse_mode="markdown")
            return
    ## Force Sub ##
    await message.reply_text(
        Localisation.HELP_MESSAGE,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Updates Channel', url='https://t.me/Discovery_Updates')
                ],
                [
                    InlineKeyboardButton('Support Group', url='https://t.me/linux_repo')
                ],
                [
                    InlineKeyboardButton('Developer', url='https://t.me/AbirHasan2005'), # Bloody Thief, Don't Become a Developer by Stealing other's Codes & Hard Works!
                    InlineKeyboardButton('Source Code', url='https://github.com/AbirHasan2005/VideoCompress') # Must Give us Credits!
                ]
            ]
        ),
        quote=True
    )
