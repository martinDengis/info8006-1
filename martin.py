from pacman_module.game import Agent, Directions
from pacman_module.util import PriorityQueue

def key(state):
    """Returns a key that uniquely identifies a Pacman game state.

    Arguments:
        state: a game state. See API or class `pacman.GameState`.

    Returns:
        A hashable key tuple.
    """

    return (
        state.getPacmanPosition(),
        tuple(state.getGhostPositions()),
        tuple(state.getCapsules()),
        state.getFood(),
    )

def manhattan_distance(point_a, point_b):
    """Returns the Manhattan distance between two points.
    
    Arguments:
        point_a: a tuple (x, y) indicating the start position.
        point_b: a tuple (x, y) indicating the goal position.
        
    Returns:
        The Manhattan distance between point A to point B.
    """
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])

def heuristic(state):
    """Returns h_cost (heuristic cost) to the closest food dot.

    Arguments:
        state: a game state. See API or class `pacman.GameState`.

    Returns:
        The lowest heuristic cost from PacMan to all remaining food dots.
    """

    min_h_cost = float('inf')
    pacman_position = state.getPacmanPosition()

    # Transform grid into list of coordinates (x, y) for True values
    goal_list = state.getFood().asList()

    # If there is no food left, heuristic is 0
    if len(goal_list) == 0:
        return 0
    
    for goal_position in goal_list:
        h_cost = manhattan_distance(pacman_position, goal_position)
        if h_cost < min_h_cost:
            min_h_cost = h_cost

    return min_h_cost

class PacmanAgent(Agent):
    """Pacman agent based on A star (A*) algorithm."""

    def __init__(self):
        super().__init__()

        self.moves = None

    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A legal move as defined in `game.Directions`.
        """

        if self.moves is None:
            self.moves = self.a_star(state)

        if self.moves:
            return self.moves.pop(0)
        else:
            return Directions.STOP
    
    def a_star(self, state):
            """Given a Pacman game state, returns a list of legal moves to solve
            the search layout.

            Arguments:
                state: a game state. See API or class `pacman.GameState`.

            Returns:
                A list of legal moves.
            """

            path = []
            fringe = PriorityQueue()
            fringe.push((state, path), heuristic(state))
            closed = set()

            while True:
                if fringe.isEmpty():
                    return []

                priority, item = fringe.pop()
                current, path = item

                if current.isWin():
                    return path

                current_key = key(current)

                if current_key in closed:
                    continue
                else:
                    closed.add(current_key)

                for successor, action in current.generatePacmanSuccessors():
                    g_cost = len(path) + 1
                    
                    # Evaluation function f(n) = g(n) + h(n)
                    f_cost = g_cost + heuristic(successor)

                    # Pushing into priority queue a tuple (state, path) and the f_cost
                    fringe.push((successor, path + [action]), f_cost)

            return path

