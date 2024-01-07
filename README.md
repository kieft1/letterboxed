# NYT Letter Boxed Solver

Python project to solve [The New York Times Letter Boxed](https://www.nytimes.com/puzzles/letter-boxed) puzzle.

## Description

The solver will construct chains of 1, 2, and 3 word solutions based on the puzzle input.

### Solver Modes

* NYT (default)
  * The solver retrieves the daily NYT game metadata and solves for 1, 2, and 3 word solutions by default.
  * This mode is optimized by retrieving the possible word list from NYT game metadata.

* Custom
  * The solver can also take a general 12 letter puzzle, three letters to a side, and solve with a few different word lists.
  * In this mode, the letters must follow the same rules of the game:
    * exactly 12 letters
    * no repeating letters
  * In order to reduce the time taken to determine solutions, the generic word lists are pared down based on these rules:
    * only containing letters from the puzzle
    * at least 3 letters in length
    * no consecutive letters from the same side of the puzzle (includes consecutive repeated letters)

## Getting Started

### Executing program

* Clone the repository
* Run letterboxed.py
* If solving the NYT puzzle, word list is saved locally
* Output of solutions saved locally

## Acknowledgments

* The NYT metadata retrieval method is based on [Alice Y. Liang's solution](https://github.com/aliceyliang/letter-boxed-solver).
* The words_easy.txt and words_hard.txt lists also came from Alice's repository (passed down from generation to generation of repos).
* Other word lists are in the repository, but can't recall where these came from.  Other repositories most likely.
