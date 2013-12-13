#!/usr/bin/env python
# encoding: utf-8

import os
import math
import sys


from collections import defaultdict

class EventStream(object):
    """
    A class for managing an un-sorted stream of events. Functions by writing
    events to disk in temporary files based on the event's record time (i.e. all
    events with a given timestamp are written to a file with that timestamp as a 
    name). By default temporary files log events by the second, but the precision 
    argument can be used to log events to a more specific timestamp decimal place.a
    In this way the memory overhead can be adjusted as needed.

    Every time the stream of events encounters an event more than 300 seconds 
    ahead of the oldest temporary file, the EventStream will load that temporary 
    file into memory, sort it, and begin emitting events in sorted order. 

    Otherwise, once the stream has been fully read, the EventStream will load the
    remaining temporary files in order, sorting and emitting events.
    
    Args:
        file_object:    the target file or stream iterable that unsorted 
                        attack records are coming from.
        precision:      the decimal precision to be used for the temporary 
                        files' timestamp 
        window:         the number of seconds within which events can be
                        expected to have arrived to the EventStream
    """
    def __init__(self, file_object, precision=0, temp_folder='temp/', 
            window=300):
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
        self.temp_folder = temp_folder
        
        self.oldest_attack = None
        self.file_dict = defaultdict(bool)

        self.file_object = file_object
        self.precision = precision
        self.window = window

    def log_event_to_disk(self, attack_time, city):
        """
        Logs an event to disk. Returns the filename the event was logged to.
        """
        #TODO: Profile performance here 
        attack_int = str(math.trunc(attack_time))
        logfile = self.temp_folder + str(math.trunc(attack_time))
        if not self.file_dict[attack_int]:
            self.file_dict[attack_int] = open(logfile, 'w')
        self.file_dict[attack_int].write(str(attack_time) + city)

    @staticmethod
    def parse_event(record):
        """
        Parses a record and returns a tuple (attack_time, city), with 
        attack_time as a float and city as a string
        """
        attack_time, city = record.strip().split('   ', 1)
        attack_time = float(attack_time)
        return attack_time, city

    @staticmethod
    def sort_second_logs(second):
        """
        Open up a logfile for a target second, load it into memory, and sort it.
        Then delete the temporary logfile and return the snapshot
        """
        #TODO
        pass

    def update_oldest_attack(self, current_record_time):
        """
        Checks to make sure our current record isn't older than our oldest 
        known attack time.
        """
        if current_record_time < self.oldest_attack or not self.oldest_attack:
            self.oldest_attack = current_record_time

    def __iter__(self):
        return self

    def next(self):
        """
        NOTES NOTES NOTES NOTES NOTES

        So, how do we want this to work exactly? 

        We only want to return an event if we are certain it is the oldest event
        not yet emitted. Where is that event? 

        If the current event is greater than 300 seconds from the oldest timestamp
        then we can pull the oldest timestamp grouping, sort it, and grab the smallest member.

        So we should have an oldest_events list? yes.







        """
        if not self.file_object:
            # If there are no more temporary files to read, stop iterating
            if len(self.file_dict.keys()) == 0:
                raise StopIteration
            else:
                pass

            """
                if self.temp_files_remaining():
                    pass
                else:
            raise StopIteration
            """
        else:
            attack_time, city = self.parse_event(self.file_object.next())
            self.log_event_to_disk(attack_time, city)
            self.update_oldest_attack(attack_time)

            return None

def event_stream(stream_obj):
    """
    Takes an interable stream object, either a file or other iterable type,
    sorts it by time, and returns the time-sorted iterable
    """
    return EventStream(stream_obj)

def update_model(event):
    """
    Updates a 怪獣 (Kaiju) model. We leave the implementation for this to
    Janet :)
    """
    pass

def main():
    """
    Main logging method
    """
    for event in event_stream(sys.stdin):
        update_model(event)
        print(event)

if __name__ == "__main__":
    main()
