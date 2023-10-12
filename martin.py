from pacman_module.game import Agent, Directions
from pacman_module.util import PriorityQueue, manhattanDistance


def key(state):
    """Returns a key that uniquely identifies a Pacman game state.

    Arguments:
        state: a game state. See API or class `pacman.GameState`.

    Returns:
        A hashable key tuple.
    """

    return (
        state.getPacmanPosition(),
        tuple(state.getCapsules()),
        state.getFood(),
    )


def heuristic(state):
    """Computes the heuristic cost for a given game state.

    The cost is calculated as the furthest distance between
    PacMan and each of the remaining food dots.

    Arguments:
        state: a game state. See API or class `pacman.GameState`.

    Returns:
        The maximum distance to a food dot.
    """

    pacman_pos = state.getPacmanPosition()

    # Consider food dots
    food_list = state.getFood().asList()
    max_dist = 0

    for food_dot in food_list:
        dist = manhattanDistance(pacman_pos, food_dot)
        if max_dist < dist:
            max_dist = dist

    return max_dist


def action_cost(state, next_state):
    """Computes the cost for moving from a given GameState to another GameState.
    
    This cost is established based on the scoring rules as follows:
        +1 for a time step
        +5 for eating a capsule

    Arguments:
        state: the current game state. See API or class `pacman.GameState`.
        next_state: the next game state. See API or class `pacman.GameState`.

    Returns:
        The g cost for the next game state
    """

    if len(state.getCapsules()) != len(next_state.getCapsules()):
        return 6    # Time cost (+1) + Eaten capsule (+5)
    
    return 1    # Time cost (+1)


class PacmanAgent(Agent):
    """Pacman agent based on A star search (A*)."""
    def __init__(self):
        super().__init__()
        self.moves = None

    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Return:
            A legal move as defined in `game.Directions`.
        """

        if self.moves is None:
            self.moves = self.astar(state)

        if self.moves:
            return self.moves.pop(0)
        else:
            return Directions.STOP

    def astar(self, state):
        """Given a Pacman game state, returns a list of legal moves to solve
        the search layout.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A list of legal moves.
        """

        path = []
        fringe = PriorityQueue()
        fringe.push((state, path, 0), heuristic(state))
        closed = set()

        while True:
            if fringe.isEmpty():
                return []

            _, (current, path, curr_g_cost) = fringe.pop()

            if current.isWin():
                return path

            current_key = key(current)

            if current_key in closed:
                continue
            else:
                closed.add(current_key)

            for successor, action in current.generatePacmanSuccessors():
                g_cost = curr_g_cost + action_cost(current, successor)

                # Evaluation function f(n) = g(n) + h(n)
                f_cost = g_cost + heuristic(successor)

                # Pushing into fringe a tuple (state, path, g_cost) and f_cost
                fringe.push((successor, path + [action], g_cost), f_cost)

        return path
