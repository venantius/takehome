package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

/*

#TODO: How do you read from stdin in Golang?

#TODO: What is a good data structure for graphs generally?

	>> Probably an adjcacency list, since we can expect this graph to be
	>> reasonably sparse. Adjacency lists are of the form {v: [v, v, v, ...]}

#TODO: How do you do breadth-first search?

#TODO: How do you identify a cyclic graph?

	>> Use Tarjan's Strongly Connected Components Algorithm (relies on DFS)

#TODO: What is a good data structures for graphs in Go?
*/

func parse(str string) (string, string, string) {
	// Breaks a statement out into its primary components
	statement := strings.Split(str, " comes ")
	country_a := statement[0]
	statement = strings.Split(statement[1], " ")
	compare := statement[0]
	country_b := strings.Join(statement[1:], "")
	return country_a, country_b, compare
}

func is_cyclic(x []string) bool {
	// In practice, this is going to be looking at a directed graph.
	//
	return true
}

func main() {
	demo_list := []string{
		"Francos comes before Anglos",
		"Francos comes after Canadio",
		"Canadio comes after Barbadonia",
		"Ethiopaea comes before Shrill Lanka"}
	for i := 0; i < len(demo_list); i++ {
		/*
			I think this might be a graph problem!

			If we treat this like a directed graph, we know that we can check for
			validity by making sure the graph doesn't contain any cycles

			Also, I think once we've confirmed that there are no cycles, we can
			initiate a breadth-first search from the top node and we should be able
			to just traverse the graph and our output should be an acceptable
			results set.
		*/
	}

	bio := bufio.NewReader(os.Stdin)
	line, truthiness, err := bio.ReadLine()
	if err == nil {
		panic("Nothing left?")
	}
	fmt.Println(line, truthiness)

	if !is_cyclic(demo_list) {
		// Normally I think we might prefer to use a panic, but we'll keep it
		// easy for now ;)
		fmt.Println("Illegal request file!")
		return
	}

	fmt.Println("Continuing...")

	/*
		for i := 0; i < len(demo_list); i++ {
			fmt.Println(demo_list[i])
		}
	*/
}
