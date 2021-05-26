# InstantInsanity_Cube
Attempt to solve an instant insanity puzzle with puzzle pieces in the shape of cubes.
This is the more common variation of the game. 
## About
This program solves for a puzzle of up to a size of 12 stacked cubes.

The puzzle is considered solved when the stack of cubes with colored sides contain no more than 1 of each color per side of the entire stack.
In a solved stack, each of the 4 sides of the stack have a unique color for every cube. 

In total each cube has 3 sets of opposite faces and the colors are enumerated. 
an example of a cube is: (1-4)(2-2)(3-5) where each (tuple) is a pair of opposite faces

If the program fails to find a solution it will find the minimum obstacle which is defined as the smallest set of cubes that cannot be solved making the whole puzzle unsolvable.

## Requirements
Python 3.0
## Design
The algorithm is a DFS/BFS style algorithm that finds all possilbe half solutions by breath first searching through all the valid half solutions in the possible solution space.
When all half solutions are found for a stack of cubes, the program finds two half soltuions which contain entire overlap in cube rotations for the stack, once 2 valid half solutions are a found the puzzle is considered solved.

If the puzzle of size 12 is unsolvable the program will continue to find the minimum obstacle
