from collections import deque
import datetime
from itertools import groupby
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
        self._book_queue = deque()
    
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
    
    def add_to_book_queue(self, start_hour, dining_no):
        self._book_queue.append((start_hour, dining_no))
        return
    
    def get_next_book(self):
        return self._book_queue[0] if self._book_queue else None
    
    def show_up(self):
        _, dining_no = self._book_queue.popleft()
        self.occupy()
        return dining_no


class TableManager(metaclass=Singleton):
    def __init__(self, clock, table_amount=6):
        self._table_amount = table_amount
        self._tables = {
            table_no: Table(table_no)
            for table_no in range(table_amount)
        }
        self._clock = clock
    
    def get_remaining_time(self, table_no):
        return self._tables[table_no].remaining_time
    
    def get_state(self, table_no):
        return self._tables[table_no].state
    
    def free_table(self, table_no):
        table = self._tables[table_no]
        table.free()
        next_book = table.get_next_book()
        if next_book is not None:
            h, _ = next_book
            if h in (self._clock.now.hour, self._clock.now.hour + 1):
                table.book()
        return

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
    
    def arrange_books(self, books):
        books.sort(key=lambda x: x[0])
        for hour, group in groupby(books, key=lambda x: x[0]):
            for table_no, (h, dining_no) in enumerate(group):
                self._tables[table_no].add_to_book_queue(h, dining_no)
        for table_no in self._tables:
            self.free_table(table_no)
        return
    
    def show_up(self, dining_no):
        for table_no, table in self._tables.items():
            next_book = table.get_next_book()
            if next_book and next_book[1] == dining_no:
                table.show_up()
                return table_no
        return None
