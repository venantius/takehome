Coding exercise
---------------

*Input:*
        
a text string containing English words, whitespace (spaces and new lines) and 
punctuation like commas, periods, question marks and semi-colons.

*For example:*

'''Hello, I like nuts. Do you like nuts? No? Are you sure? 
Why don't you like nuts? Are you nuts? I like you'''


*Output:*

Print a list of triplets. Each triplet is a pair of words and a count

For example the output for the sample input:

Are you: 2

like nuts: 3

you like: 3

I like: 2

A pair of words should show up in the output if one of the words follows the
other in the input and are separated only by whitespace. Every pair that shows
up more than once should have an entry in the output with the correct number of
occurrences. Note, that the order of the words in the pair doesn't matter:  
'green bee' and 'bee green' are 2 occurrences of the same pair. Ignore case. 
'BlUe sKY' is the same pair as 'SKy bLUE'.

*Your mission if you choose to accept it:*

Write a function that accepts the input and produces the output

*Guidelines:*

 - If something is unclear ask for clarification
 - Write down any assumption you make
 - Write good, correct, readable code.
 - Focus on the logic of the program
 - If you write tests include them as well
 - Don't worry about performance
