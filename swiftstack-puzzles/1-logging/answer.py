#!/usr/bin/env python
# encoding: utf-8

"""
This is a solution to the SwiftStack Puzzle #1 (Logging). Either of the 
following usage methods will work.

USAGE:
    cat sample_record_file | python answer.py
    python answer.py sample_record_file
"""

import fileinput
import heapq
import sys

class EventStream(object):
    """
    A class for managing an un-sorted stream of events. Functions by holding events
    in memory until an event comes in that is newer than the oldest event, at which 
    point it emits the oldest events until the window has been closed again.

    Args:
        input_stream:   the target file or stream iterable that unsorted 
                        attack records are coming from.
        window:         the number of seconds within which events can be
                        expected to have arrived to the EventStream
    """
    def __init__(self, input_stream, window=300):
        self.attack_heap = []
        self.oldest_attack = None
        self.latest_record = None
        self.input_stream = input_stream
        self.window = window

    @staticmethod
    def parse_event(record):
        """
        Parses a record and returns a tuple (attack_time, city), with 
        attack_time as a float and city as a string
        """
        attack_time, city = record.strip().split('   ', 1)
        attack_time = float(attack_time)
        return attack_time, city

    def emit_oldest_attack(self):
        """
        Formats an attack record from the heap as a string for printing.
        """
        record = heapq.heappop(self.attack_heap)
        # Format our floats so that Python doesn't truncate them
        record = ("{:10.6f}".format(record[0]), record[1])
        record = '   '.join([str(x) for x in record])
        return record

    def update_oldest_attack(self, current_record_time):
        """
        Checks to make sure our current record isn't older than our oldest 
        known attack time.
        """
        if not self.oldest_attack or current_record_time < self.oldest_attack:
            self.oldest_attack = current_record_time

    def __iter__(self):
        return self

    def next(self):
        """
        Emit the oldest record by attack time in the input stream.

        In general, this can only be safely done once an attack record more
        recent than our uncertainty window has been observed, or when we've
        reached the end of our input stream.
        """
        if self.input_stream:
            if len(self.attack_heap) == 0:
                self.oldest_attack = None

            while (not self.oldest_attack) or \
                    (self.latest_record - self.oldest_attack < self.window):
                try:
                    record = self.input_stream.next()
                    attack_time, city = record.strip().split('   ', 1)
                    attack_time, city = self.parse_event(record)
                except StopIteration:
                    self.input_stream = None
                    break
                heapq.heappush(self.attack_heap, (attack_time, city))
                self.update_oldest_attack(attack_time)
                self.latest_record = attack_time

            return self.emit_oldest_attack()

        elif len(self.attack_heap) > 0:
            return self.emit_oldest_attack()

        else:
            raise StopIteration

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

def main(args):
    """
    Main logging method
    """
    for event in event_stream(fileinput.input(args)):
        update_model(event)
        print(event)

if __name__ == "__main__":
    main(sys.argv[1:])
