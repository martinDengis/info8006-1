from pacman_module.game import Agent, Directions
import heapq  # For using a priority queue (heap)

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
    """
    Calculate the Manhattan distance from Pacman's position to the nearest food.

    Arguments:
        state: a game state. See API or class `pacman.GameState`.

    Returns:
        An integer representing the heuristic value.
    """
    pacManPosition = state.getPacmanPosition()
    foodGrid = state.getFood()
    foodPositions = foodGrid.asList()  # Get the coordinates of all food pieces
    
    # If there is no food left, heuristic is 0
    if len(foodPositions) == 0:
        return 0
    
    # Calculate the Manhattan distance to the closest food
    closestFoodDist = min(abs(x1 - x2) + abs(y1 - y2) for x1, y1 in [pacManPosition] for x2, y2 in foodPositions)
    
    return closestFoodDist

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
        """
        Implements the A* search algorithm to find an optimal path from the
        current state to the goal (winning) state.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A list of legal moves to reach the goal state.
        """
        path = []  # To keep track of the path
        fringe = []  # Fringe to store the nodes to explore (using heapq to keep it ordered)
        # Heapq uses the first element of the tuple for ordering. 
        # Our tuple: (f, g, counter, state, path) where f = g + heuristic(state)
        heapq.heappush(fringe, (0 + heuristic(state), 0, 0, state, path))  # (f, g, counter, state, path)
        closed = set()  # Set to store explored nodes
        counter = 0  # Counter to avoid comparing GameState instances

        while True:  # Keep searching until solution found or no solution exists
            if not fringe:  # No solution exists
                return []

            f, g, _, current, path = heapq.heappop(fringe)  # Get node with smallest 'f' value

            if current.isWin():  # Solution found
                return path
            
            current_key = key(current)  # Generate a unique key for the current state
            
            if current_key in closed:  # Skip if state already explored
                continue
            closed.add(current_key)  # Mark state as explored

            # Generate successor states and add them to the fringe
            for successor, action in current.generatePacmanSuccessors():
                new_path = path + [action]  # Create new path
                new_g = g + 1  # Increment cost so far
                counter += 1  # Increment counter
                # Add successor to fringe with updated costs and path
                heapq.heappush(fringe, (new_g + heuristic(successor), new_g, counter, successor, new_path))

        return path
