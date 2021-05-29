import datetime
from lineup_queue import Singleton

class Clock(metaclass=Singleton):
    def __init__(self):
        self._absolute_start = datetime.datetime.now()
        self._relative_start = datetime.datetime.combine(
            datetime.date.today(),
            datetime.time(13, 0, 0)
        )
        
    @property
    def now(self):
        elapsed = datetime.datetime.now() - self._absolute_start
        return (self._relative_start + elapsed).time()
