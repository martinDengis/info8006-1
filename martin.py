from pacman_module.game import Agent, Directions


class PacmanAgent(Agent):
    """Pacman agent absed on A* algorithm."""

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
        open = set()
        closed = set()

        while True:
            current = open.pop(lowest f_cost)
            closed.add(current)

            if current.isWin():
                return path
            
            neighbours = current.getNeighbours()
            for neighbour in neighbours:
                if neighbour in closed:
                    continue

                # Check if neighbour is not traversable (get Grid and check boolean at position (x,y) for neighbour)
                if Grid.neighbour == 1:
                    continue

                if (new path to neighbour is shorter) or (neighbour is not in open):
                    neighbour.f_cost = newCost(to determine)
                    neighbour.parent = current
                    if neighbour is not in open:
                        open.add(neighbour)
                    

""" Pseudocode for A* """
# OPEN //the set of nodes to be evaluated
# CLOSED //the set of nodes already evaluated
# add the start node to OPEN

# loop
#     current = node in OPEN with the lowest f_cost
#     remove current from OPEN
#     add current to CLOSED

#     if current is the target node //path has been found
#         return

#     foreach neighbour of the current node
#         if neighbour is not traversable or neighbour is in CLOSED
#             skip to the next neighbour

#         if new path to neighbour is shorter OR neighbour is not in OPEN
#             set f_cost of neighbour
#             set parent of neighbour to current
#             if neighbour is not in OPEN
#                 add neighbour to OPEN

# https://saturncloud.io/blog/implementing-the-a-algorithm-in-python-a-stepbystep-guide/#:~:text=Implementing%20the%20A%2A%20Algorithm%20in%20Python%201%20Node,itself.%20...%204%20Putting%20It%20All%20Together%20