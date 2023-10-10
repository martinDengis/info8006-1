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


def heuristic(state):
    """ This function should aim at minimizing the remaining cost of the game.
    => Check remaining_cost estimate"""
    if state.isWin():
        return 0  # If the game is won, no remaining cost

    if state.isLose():
        return float('inf')  # If the game is lost, return positive infinity as heuristic (maximum cost)

    pacman_position = state.getPacmanPosition()
    food_positions = state.getFood().asList()

    # Calculate the remaining cost based on the provided scoring rules : Goal is to MINIMIZE the remaining cost
    remaining_cost = (
        5 * state.getNumFood() +  # Eating food dots is undesirable (for remaining cost), so we use a positive weight
        -5 * len(state.getCapsules()) +  # Eating capsules is desirable, so we use a negative weight
        - 1 * to_closest_food_dot(pacman_position, food_positions)
    )

    return remaining_cost


def to_closest_food_dot(pacman_position: tuple, food_positions: list):
    if not food_positions:
        return 0
    
    if len(food_positions) == 1:
        return manhattanDistance(pacman_position, food_positions[0])
    
    min_distance = float('inf')
    min_index = 0
    for i, item in enumerate(food_positions):
        dist = manhattanDistance(pacman_position, item)
        if dist < min_distance:
            min_distance = dist
            min_index = i

    new_pacman_position = food_positions.pop(min_index)
    return min_distance + to_closest_food_dot(new_pacman_position, food_positions)

# def to_furthest_food_dot(pacman_position: tuple, food_positions: list):
#     if not food_positions:
#         return 0
    
#     if len(food_positions) == 1:
#         return manhattanDistance(pacman_position, food_positions[0])
    
#     max_distance = float('-inf')
#     max_index = 0
#     for i, item in enumerate(food_positions):
#         dist = manhattanDistance(pacman_position, item)
#         if dist > max_distance:
#             max_distance = dist
#             max_index = i

#     new_pacman_position = food_positions.pop(max_index)
#     return max_distance + to_furthest_food_dot(new_pacman_position, food_positions)

""" Iterative function """
# def to_furthest_food_dot(pacman_position: tuple, food_positions: list):
#     total_distance = 0
    
#     while food_positions:
#         max_distance = float('-inf')
#         max_index = None
        
#         for i, food_position in enumerate(food_positions):
#             dist = manhattanDistance(pacman_position, food_position)
#             if dist > max_distance:
#                 max_distance = dist
#                 max_index = i
        
#         if max_index is not None:
#             total_distance += max_distance
#             pacman_position = food_positions.pop(max_index)
    
#     return total_distance


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
                f_cost = g_cost + heuristic(successor)

                # Pushing into priority queue a tuple (state, path) and the f_cost
                fringe.push((successor, path + [action]), f_cost)

        return path
