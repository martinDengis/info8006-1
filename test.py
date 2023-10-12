from pacman_module.game import Agent, Directions
from pacman_module.util import PriorityQueue, manhattanDistance


def key(state):
    """
    Returns a key that uniquely identifies a Pacman game state.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.

    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state.
    """

    # TODO
    return state.getPacmanPosition(), state.getFood(), tuple(state.getCapsules())


def step_cost(prev_state, next_state):
    if len(prev_state.getCapsules()) > len(next_state.getCapsules()):
        return 6    # We have eaten a big capsule so 5 points
    else:
        return 1    # If we add 1, we get bfs because we add a depth of one


def heuristic(state):
    food_grid = state.getFood()
    pacman_pos = state.getPacmanPosition()
    distances = []

    for x in range(food_grid.width):
        for y in range(food_grid.height):
            if food_grid[x][y]:
                distances.append(manhattanDistance(pacman_pos, (x, y)))

    if not distances:
        return 0
    else:
        return max(distances)


class PacmanAgent(Agent):
    """
    A Pacman agent based on Depth-First-Search.
    """

    def __init__(self):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        super().__init__()
        self.moves = []

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        if not self.moves:
            self.moves = self.astar(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

    def astar(self, state):
        """
        Given a pacman game state,
        returns a list of legal moves to solve the search layout.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A list of legal moves as defined in `game.Directions`.
        """

        path = []
        fringe = PriorityQueue()
        fringe.push((state, path, 0.), 0.)

        closed = set()

        while True:
            if fringe.isEmpty():
                return []

            _, (current, path, cost) = fringe.pop()

            current_key = key(current)

            if current.isWin():
                return path

            if current_key not in closed:
                closed.add(current_key)

                for next_state, action in current.generatePacmanSuccessors():
                    next_cost = cost + step_cost(current, next_state)
                    fringe.push((next_state, path + [action], next_cost), next_cost +
                                heuristic(next_state))
