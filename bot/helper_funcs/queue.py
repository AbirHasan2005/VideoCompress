# (c) @AbirHasan2005 | @ballicipluck

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import sys
from bot import LOG_CHANNEL


class Queues:
    Q = []
    IS_BUZY = False

    async def check_queue(self, update: Message = None):  # None given cuz update only needed if bot is busy.
        from bot.helper_funcs.compress import _compress  # recursive imports :fp
        # Maybe use property instead. Would be better and safer for incomplete downloads with db support.

        if Queues.IS_BUZY: 
            await update.reply_text(
                'Your File Added to Queue!\nWait till I start Compressing.',
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Show Bot Status', url=f'https://t.me/{LOG_CHANNEL}')
                        ]
                    ]
                )
            )  # maybe add a button to query number of items left in queue // position in queue
        else:
            try:
                q = Queues.Q[0]
            except IndexError:  # meaning queue is empty
                return
            Queues.IS_BUZY = True
            await _compress(q.bot, q.update, q.isAuto, q.target_percentage)


class Queue_Item:  # just to provide a schema for items added in queue
    def __init__(self, bot, update, isAuto, target_percentage):
        self.bot = bot
        self.update = update
        self.isAuto = isAuto
        self.target_percentage = target_percentage
        Queues.Q.append(self)
        print(sys.getsizeof(Queues.Q))
