import re
import sys
import time
import datetime
import threading

default = '/home/francesco/repos/trivial_textual_time_tracker/log'
continue_ = True

def points(seconds=60):
    while continue_:
        for s in range(seconds):
            if continue_: time.sleep(1)
        print('.', end='')
        sys.stdout.flush()

def prompt(now, interval=None):
    '''
    Start waiting a new description from the user. Show to the user a new slot
    where to write the description of current task.
    '''
    if interval: print(interval)
    print()
    print(now)

class FileManager:
    def __init__(self, argv):
        try:
            position  = default or argv[1]
            self.file = open(position, 'a')
        except Exception as e:
            print('Caught exception "{0}", not writing the log to the filesystem'.format(e))
            self.file = None

    def new_record(self, *args):
        if self.file:
            record = self.format_record(*args)
            self.file.write('{0}\n'.format(record))
            self.file.flush()

    @staticmethod
    def format_record(number, description, date=None):
        '''
        >>> FileManager.format_record(33, 'a #long description\\n', datetime.datetime(2012, 2, 1, 16, 41, 59, 369339))
        '33, a #long description, 2012-02-01 16:41:59.369339'
        '''
        description = re.sub('\n', '', description)
        fields      = map(str, (number, description, date))
        return ', '.join(fields)

if __name__=='__main__':
    f=FileManager(sys.argv)
    t=threading.Thread(None, points)
    t.start()
    now = datetime.datetime.now()
    prompt(now)
    for line in sys.stdin:
        before   = now
        now      = datetime.datetime.now()
        interval = now - before
        interval = round(interval.seconds/60)
        f.new_record(interval, line, now)
        prompt(now, interval)
    continue_ = False
    print('Please wait while our pointer is finishing pointing...')
