from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from bot import LOG_CHANNEL

class Queues:
    Q = []
    IS_BUZY = False

    async def check_queue(update = None):
        from bot.helper_funcs.compress import _compress
        if Queues.IS_BUZY:
            await update.reply_text(
                'Added to queue. ',
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Show Bot Status', url=f'https://t.me/{LOG_CHANNEL}')
                        ]
                    ]
                )
            )
        else:
            try:
                q = Queues.Q.pop(0)
            except IndexError:
                return
            Queues.IS_BUZY = True
            await _compress(q.bot, q.update, q.isAuto, q.target_percentage)


class Queue_Item:
    def __init__(self, bot, update, isAuto, target_percentage):
        self.bot = bot
        self.update = update
        self.isAuto = isAuto
        self.target_percentage = target_percentage
    
    def _add(self):
        try:
            Queues.Q.append(self)
            return 1
        except Exception as e:
            print(e)
            return 0
    