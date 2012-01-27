import sys
import time
import datetime
import threading

default = ''
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

    def new_record(self, number, string):
        if self.file:
            record = self.format_record(number, string)
            self.file.write(record)

    @staticmethod
    def format_record(number, string):
        '''
        >>> format_record(33, 'a long description')
        33, a long description
        '''
        return '{0}, {1}'.format(number, string)

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
        f.new_record(interval, line)
        prompt(now, interval)
    continue_ = False
    print('Please wait while our pointer is finishing pointing...')
