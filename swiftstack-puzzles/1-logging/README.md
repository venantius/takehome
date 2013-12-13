[Logging is Awesome](/Users/jarvis/Documents/dev/takehome/swiftstack-puzzles/1-logging)
==================


Face it -- log processing is a riot. Everyone wants the log processing jobs because everyone knows that log processing is the most fun you can have outside of a glass of white wine and a bubble bath. 

Everyone, that is, except for Janet.

Janet's got a log processing problem and she needs help. She's got a very important program whose sole purpose is to predict which city Gamera, and other Gameralike monsters, will attack next.

(It will later be extended to support other flying creatures such as Godzillas and Flying King Kongs. Mothra's case, though, is trivial -- whichever city is the best lit.)

Her datafile is a stream of events and times that represent cities that Gamera has destroyed in the past:

```
1363359470.629802 San Bernardino, CA, USA
1363359471.848128 Paris, TX, USA
1363359468.727172 Verona, Italy
1363359440.991101 Kyoto, Japan
```

Her processing loop looks like this:

```
for event in event_stream(filename):
    update_model(event)
    print(event)
```

She'd like you to write the event_stream() method. Simple enough. But Janet has a problem. Due to the proliferation of Gamera and Gameralike monsters, sightings occur all over the world, and the sheer quantity of data is staggering -- she can't possibly hold it all in memory. Furthermore, since the data is streaming in from many different sources, she can't guarantee that they're arriving in chronological order (as the model requires) inside of any 300 second window.

Can you write her a method that minimizes processing time and memory use but returns the events in order?

You can use this program to generate sample logfiles:

```
import time
import random

JITTER = 275 
TICKS = 1000
LINES_PER_TICK = 1000

def log_line(now):
    timestamp = now - (random.random() * JITTER)
    return "%f   City %d" % (timestamp, random.randint(0,10000))

start = time.time()

for tick in xrange(TICKS):
    now = start + tick
    for num_line in xrange(LINES_PER_TICK):
    print(log_line(now))
```
