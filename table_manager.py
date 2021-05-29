import datetime
from lineup_queue import Singleton



class Table:
    def __init__(
        self,
        table_no, 
        state='empty', 
        duration=60, 
    ):
        self._table_no = table_no
        self._duration = duration
        self._state = state
    
    @property
    def table_no(self):
        return self._table_no
    
    @property
    def state(self):
        return self._state
    
    @property
    def remaining_time(self):
        if self.state != 'occupied':
            return datetime.time(minute=59, second=59)
        now = datetime.datetime.now()
        elapsed_time = now - self._now
        self._now = now
        self._remaining_time -= elapsed_time
        minute, second = divmod(self._remaining_time.seconds, 60)
        return datetime.time(minute=minute, second=second)
    
    def occupy(self):
        self._state = 'occupied'
        self._init_time()
        return
    
    def _init_time(self):
        self._now = datetime.datetime.now()
        self._remaining_time = datetime.timedelta(minutes=self._duration)
        return
    
    def free(self):
        self._state = 'empty'
    
    def book(self):
        self._state = 'booked'
    
    def is_empty(self):
        return self._state == 'empty'
    
    def is_booked(self):
        return self._state == 'booked'
    
    def is_occupied(self):
        return self._state == 'occupied'


class TableManager(metaclass=Singleton):
    def __init__(self, table_amount=6):
        self._table_amount = table_amount
        self._tables = {
            table_no: Table(table_no)
            for table_no in range(table_amount)
        }
    
    def get_remaining_time(self, table_no):
        return self._tables[table_no].remaining_time
    
    def get_state(self, table_no):
        return self._tables[table_no].state
    
    def free_table(self, table_no):
        self._tables[table_no].free()
    
    def occupy_table(self, table_no):
        if self._tables[table_no].is_empty():
            self._tables[table_no].occupy()
        return
    
    def get_empty_table(self):
        picked_table = None
        for table_no, table in self._tables.items():
            if table.is_empty():
                picked_table = table_no
        return picked_table
