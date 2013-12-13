[Puzzle #3: I Love A Parade](http://swiftstack.com/jobs/puzzles/parade/)
===========================
Every year on the planet Boron, all the nations of the world meet at Le Grand Faire. 
Many nations send full delegations and floats to participate in the Great Parade,
an event that is watched with rapt attention and delight throughout the globe.

Such an event cannot be without politics. Many nations have strong opinions
regarding where their float should be placed in the parade, particularly relative to
the placement of other nations. For instance: Francos wants to be before 
Anglos, their main rival, but this year they want to be after Canadio, because
their float makes fun of Canadionians.

They each send their requests in to the Central Parade Committee, which decides
whether or not to accept or reject their bribes and consolidates the accepted
requests into a master list. Then they send that list on to you, the underpaid
intern. From you, they expect a parade order that meets all of the constraints 
given. Little do they know that you have the power of $YOUR_FAVORITE_LANGUAGE
at your disposal!

Their list comes in the form of a large, properly formatted data file with the 
following structure:

```
Francos comes before Anglos
Francos comes after Canadio
Canadio comes after Barbadonia
Ethiopaea comes before Shrill Lanka
```

Your output should come as a list that satisfies the constraints given. For example,
for the above requests, your program could print:

```
Ethiopaea
Barbadonia
Canadio
Francos
Anglos
Shrill Lanka
```

Many other orderings are, of course, equally viable. Not all sets of requests
are legal, however. If, for instance, the request file was:

```
Francos comes before Anglos
Anglos comes before Francos
```

Then your program should print:

Illegal request file!
And be done with it.


