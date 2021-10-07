# Eight Puzzle
## Overview
The classic 8 puzzle game built in Python using Pygame. The game consists of 9 tiles in a 3x3 grid. 
There are 8 tiles numbered 1-8 and an empty tile. The goal is to move the empty tile around the board
until all tiles are in numerical order with the empty tile at the end. When the player wins, the board
will turn green.

## Example

<table>
<tr><th>Initial State </th><th>Goal State</th></tr>
<tr>
<td>
    <table>
        <tr>
            <td>1</td><td>6</td><td>2</td>
        </tr>
        <tr>
            <td></td><td>4</td><td>5</td>
        </tr><tr>
            <td>3</td><td>8</td><td>7</td>
        </tr>
    </table>
</td>
<td>
    <table>
        <tr>
            <td>1</td><td>2</td><td>3</td>
        </tr>
        <tr>
            <td>4</td><td>5</td><td>6</td>
        </tr>
        <tr>
            <td>7</td><td>8</td><td></td>
        </tr>
    </table>
</td>
</tr>
</table>

## How to Play
The player can move the empty tile around the board by clicking on adjacent tiles to swap with.
The player wins once all tiles are in numerical order with the blank tile at the end. 
If the player is unable to solve the puzzle, they may choose a pathfinding algorithm to help find 
a path to the goal.

Press 'R' to generate a new random puzzle. 

### Solve
#### A* Algorithm
Press 'M' for the A* algorithm. This algorithm uses a heuristic function to guide which moves
should be selected. The heuristic value for each possible move is calculated by the number of tiles out of place and 
the Manhattan distance. The best state is then selected based on depth and best heuristic value. 