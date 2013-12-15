[It's a Python Party!](http://swiftstack.com/jobs/puzzles/party/)
======================
John Partyson is the CEO at PartyCo, and he wants to celebrate a
record-breaking year with a company party. Not just any company party,
though; the best company party possible, as befits a company called
PartyCo.

To that end, he's come up with a party-animal score for every employee
of PartyCo. The party-animal score is a number, and the higher the
party-animal score, the more fun that the employee will contribute to
a party. Party-animal scores may be positive, negative, or zero.

However, John Partyson knows that who you party with is important. If
an employee's boss is at a party, then the employee will spend all
their time looking over their shoulder for their boss, and that's not
fun. Therefore, at this company party, no employee and their boss will
both be invited. A boss's boss is okay, but you can't have both an
employee and their boss.

Your task, as a PartyCo programmer, is to write a program that takes
in an employee listing and outputs the guests to invite in order to
maximize the sum of the guests' party-animal scores.

The input will be given to your program on standard input as a JSON
document in the following form:

```
[
    {
        "name": "John Partyson",
        "boss": null,
        "party-animal-score": 57.1
    },
    {
        "name": "Steve McFunGuy",
        "boss": "John Partyson",
        "party-animal-score": 12.2
    },
    # ... and so on
]
```

Your program must print, on standard output, the names of the
employees to include in the party. Print one name per line; the names
do not need to be in any particular order.

No two employees will have the same name, so there is no need to worry
about name collisions.

Each employee has exactly one boss and appears in the input exactly
one time except for the CEO, who has no boss.

PartyCo is going to sell your code as a service to other companies, so
do not assume that the CEO is always named John Partyson.

For bonus points: ensure that your solution always invites the CEO.

Example Input 1:
```
[
{
"name": "Al Buquerque",
"boss": null,
"party-animal-score": 2.0
},
{
"name": "Ferb Jinglemore",
"boss": "Al Buquerque",
"party-animal-score": 12.1
},
{
"name": "Click N. Clack",
"boss": "Al Buquerque",
"party-animal-score": 34.3
},
{
"name": "Carl Balgruuf",
"boss": "Ferb Jinglemore",
"party-animal-score": -0.4
},
{
"name": "Moe Shroom",
"boss": "Carl Balgruuf",
"party-animal-score": 44.91
},
{
"name": "Jerky McGetsDrunkAndPeesInYourFridge",
"boss": "Carl Balgruuf",
"party-animal-score": -9999.99
},
{
"name": "Howard M. Burgers",
"boss": "Click N. Clack",
"party-animal-score": 14.4
},
{
"name": "Soren de Kiester",
"boss": "Click N. Clack",
"party-animal-score": 25
}
]
```

Sample Output 1 (normal):
```
Ferb Jinglemore
Moe Shroom
Howard M. Burgers
Soren de Kiester
```

Sample Output 1 (making sure to invite the CEO):
```
Al Buquerque
Moe Shroom
Howard M. Burgers
Soren de Kiester
```
