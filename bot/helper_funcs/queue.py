from bot.helper_funcs.compress import _compress

class Queues:
    Q = []
    IS_BUZY = False

    def check_queue(self):
        if self.IS_BUZY:
            pass
        else:
            try:
                q = Queues.Q.pop(0)
            except IndexError:
                return
            self.IS_BUZY = True
            _compress(q.bot, q.update, q.isAuto, q.target_percentage)


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
    