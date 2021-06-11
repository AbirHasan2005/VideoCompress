from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


class Queues:
    Q = []
    IS_BUZY = False

    async def check_queue(update):
        from bot.helper_funcs.compress import _compress
        if Queues.IS_BUZY:
            update.reply_text(
                'Added to queue. ',
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Show Bot Status', url=f'https://t.me/{LOG_CHANNEL}')
                        ]
                    ]
                )
            )
            await bot.send_message(
                chat_id=update.chat.id,
                text=Localisation.FF_MPEG_RO_BOT_STOR_AGE_ALREADY_EXISTS,
                
                reply_to_message_id=update.message_id
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
    