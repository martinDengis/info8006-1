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
        tuple(state.getGhostPositions()),
        tuple(state.getCapsules()),
        state.getFood(),
        # state.getPacmanState().getDirection()
    )


def heuristic(state):
    """Computes the heuristic score for a given game state.

    The score is calculated based on the current game score,the distance to
    the closest food dot, and the distance to the closest capsule. The number
    of remaining food dots and capsules are also considered.

    Arguments:
        state: The current game state.

    Returns:
        The negative of the calculated score. A higher score is better.
    """

    score = state.getScore()
    pos = state.getPacmanPosition()

    # Consider food dots
    foodList = state.getFood().asList()
    closestFoodDist = float('inf')

    if foodList:
        # Find distance to closest food dot based on the Manhattan Distance
        closestFoodDist = min(
            [manhattanDistance(pos, food) for food in foodList]
            )
        score += 10 * len(foodList)

    # Consider capsules
    capsuleList = state.getCapsules()
    if capsuleList:
        # Find distance to closest capsule based on the Manhattan Distance
        closestCapsuleDist = min(
            [manhattanDistance(pos, capsule) for capsule in capsuleList]
        )
        # Check if a capsule is on the shortest path to the nearest food dot
        if closestCapsuleDist <= closestFoodDist:
            # Reduce the score to make sure the final path chosen is optimal
            score -= 5 * len(capsuleList)

    return -score


class PacmanAgent(Agent):
    def __init__(self):
        super().__init__()
        self.moves = None

    def get_action(self, state):
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

                # Pushing into priority queue a tuple (state, path) and f_cost
                fringe.push((successor, path + [action]), f_cost)

        return path
