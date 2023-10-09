from pacman_module.util import PriorityQueue
from pacman_module.game import Agent, Directions


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
    if state.getNumFood() == 0:
        return 0
    
    pacman_position = state.getPacmanPosition()
    unvisited_food = state.getFood().asList()
    capsules = state.getCapsules()

    # Calculate the distance to the nearest unvisited food dot
    nearest_food_dist = min(manhattan_distance(pacman_position, food_pos) for food_pos in unvisited_food)

    # Calculate the distance to the nearest capsule
    nearest_capsule_dist = min(manhattan_distance(pacman_position, capsule_pos) for capsule_pos in capsules)

    # Combine both distances to get the heuristic value
    heuristic_value = nearest_food_dist + nearest_capsule_dist

    return heuristic_value



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
        path = []
        fringe = PriorityQueue()
        fringe.push((state, path), 0)  # Start with a heuristic cost of 0
        closed = set()
        unvisited_food = state.getFood().asList()  # Get all unvisited food dots


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
                
                # Calculate the heuristic dynamically to the nearest unvisited food dot and nearest capsule
                nearest_food_dist = min(manhattan_distance(successor.getPacmanPosition(), food_pos) for food_pos in unvisited_food)
                nearest_capsule_dist = min(manhattan_distance(successor.getPacmanPosition(), capsule_pos) for capsule_pos in state.getCapsules())
                f_cost = g_cost + nearest_food_dist + nearest_capsule_dist

                # Pushing into priority queue a tuple (state, path) and the f_cost
                fringe.push((successor, path + [action]), f_cost)

        return path
