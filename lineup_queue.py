from collections import deque



class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LineupQueue(metaclass=Singleton):
    def __init__(self):
        self._lineup_no = 0
        self._showup_no = 0
        self._queue = deque()

    def take_lineup_no(self):
        lineup_no = str(self._lineup_no).zfill(3)
        self._queue.append(lineup_no)
        self._lineup_no += 1
        return lineup_no

    def take_showup_no(self):
        showup_no = f'b{str(self._showup_no).zfill(3)}'
        self._showup_no += 1
        return showup_no

    def get_next_dining_no(self):
        return self._queue.popleft()
    
    def is_empty(self):
        return not self._queue
