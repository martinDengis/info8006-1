from pacman_module.game import Agent, Directions
from pacman_module.util import PriorityQueue, manhattanDistance
import heapq  # For using a priority queue (heap)
import networkx as nx


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

# def heuristic(state):
#     # Get current position
#     pos = state.getPacmanPosition()

#     # Consider food dots
#     foodList = state.getFood().asList()

#     # Create a graph with food dots as nodes and Manhattan distances as edges
#     G = nx.Graph()
#     for i in range(len(foodList)):
#         for j in range(i+1, len(foodList)):
#             dist = manhattanDistance(foodList[i], foodList[j])
#             G.add_edge(i, j, weight=dist)

#     # Calculate Minimum Spanning Tree (MST)
#     mst = nx.minimum_spanning_tree(G)

#     # Use total weight of MST as heuristic
#     heuristic = sum([data['weight'] for (_, _, data) in mst.edges(data=True)])

#     # Consider capsules
#     capsuleList = state.getCapsules()
#     if capsuleList:
#         # Find distance to closest capsule
#         closestCapsuleDist = min([manhattanDistance(pos, capsule) for capsule in capsuleList])
#         # Subtract 5 from heuristic for each remaining capsule
#         heuristic -= 5 * len(capsuleList)

#     return heuristic

def heuristic(state):
    # Initialize score to current game score
    score = state.getScore()

    # Get current position
    pos = state.getPacmanPosition()

    # Consider food dots
    foodList = state.getFood().asList()
    closestFoodDist = float('inf')

    if foodList:
        # Find distance to closest food dot
        closestFoodDist = min([manhattanDistance(pos, food) for food in foodList])
        # Add number of remaining food dots times 10 from score
        # Subtract distance to closest food dot from score
        score += 10 * len(foodList)

    # Consider capsules
    capsuleList = state.getCapsules()
    if capsuleList:
        # Find distance to closest capsule
        closestCapsuleDist = min([manhattanDistance(pos, capsule) for capsule in capsuleList])
        # Check if a capsule is on the shortest path to the nearest food dot
        if closestCapsuleDist <= closestFoodDist:
            # Subtract number of remaining capsules times 5 from score
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
