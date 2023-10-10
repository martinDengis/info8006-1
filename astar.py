from pacman_module.util import PriorityQueue, manhattanDistance
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


# def heuristic(state):
#     """Returns h_cost (heuristic cost) to the closest food dot.

#     Arguments:
#         state: a game state. See API or class `pacman.GameState`.

#     Returns:
#         The lowest heuristic cost from PacMan to all remaining food dots.
#     """

#     # If there is no food left, heuristic is 0
#     if state.getNumFood() == 0:
#         return 0
    
#     min_h_cost = float('inf')
#     pacman_position = state.getPacmanPosition()

#     # Transform grid into list of coordinates (x, y) for True values
#     goal_list = state.getFood().asList()
#     capsule_list = state.getCapsules()

#     for goal_position in goal_list:
#         h_cost = manhattanDistance(pacman_position, goal_position)
#         for capsule_position in capsule_list:
#             if manhattanDistance(pacman_position, capsule_position) + manhattanDistance(capsule_position, goal_position) <= h_cost:
#                 # Add a penalty for passing through a capsule
#                 h_cost += 100  # Set the penalty value to 5

#         if h_cost < min_h_cost:
#             min_h_cost = h_cost

#     return min_h_cost

def heuristic(state, path):
    """ This function should aim at minimizing the remaining cost of the game.
    => Check remaining_cost estimate"""
    if state.isWin():
        return 0  # If the game is won, no remaining cost

    if state.isLose():
        return float('inf')  # If the game is lost, return positive infinity as heuristic (maximum cost)

    food_positions = state.getFood().asList()

    # Calculate the remaining cost based on the provided scoring rules
    remaining_cost = (
        -10 * state.getNumFood() +  # Eating food dots is desirable, so we use a negative weight
        5 * len(state.getCapsules()) +  # Eating capsules is undesirable, so we use a positive weight
        to_furthest_food_dot(state.getPacmanPosition(), food_positions)
    )

    return remaining_cost

def to_furthest_food_dot(pacman_position: tuple, food_positions: list):
    if not food_positions:
        return 0
    
    if len(food_positions) == 1:
        return manhattanDistance(pacman_position, food_positions[0])
    
    max_distance = float('-inf')
    max_index = 0
    for i in range(len(food_positions)):
        dist = manhattanDistance(pacman_position, food_positions[i])
        if dist > max_distance:
            max_distance = dist
            max_index = i

    new_pacman_position = food_positions.pop(max_index)
    return max_distance + to_furthest_food_dot(new_pacman_position, food_positions)


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
        fringe.push((state, path), heuristic(state, path))
        closed = set()

        while True:
            if fringe.isEmpty():
                return []

            priority, item = fringe.pop()
            current, path = item

            if current.isWin():
                # print(path)
                return path

            current_key = key(current)

            if current_key in closed:
                continue
            else:
                closed.add(current_key)

            for successor, action in current.generatePacmanSuccessors():
                g_cost = len(path) + 1
                
                # Evaluation function f(n) = g(n) + h(n)
                f_cost = g_cost + heuristic(successor, path)

                # Pushing into priority queue a tuple (state, path) and the f_cost
                fringe.push((successor, path + [action]), f_cost)

        return path
