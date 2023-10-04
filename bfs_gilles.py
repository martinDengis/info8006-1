from pacman_module.game import Agent, Directions
from pacman_module.util import Queue

def key(state):
    return (
        state.getPacmanPosition(),
        tuple(state.getGhostPositions()),
        tuple(state.getCapsules()),
        state.getFood(),
    )

class PacmanAgent(Agent):
    def __init__(self):
        super().__init__()
        self.moves = None

    def get_action(self, state):
        if self.moves is None:
            self.moves = self.bfs(state)

        if self.moves:
            return self.moves.pop(0)
        else:
            return Directions.STOP

def bfs(self, state):
    """Given a Pacman game state, returns a list of legal moves to solve
    the search layout.

    Arguments:
        state: a game state. See API or class `pacman.GameState`.

    Returns:
        A list of legal moves.
    """

    path = []
    fringe = Queue() 
    fringe.push((state, path))
    closed = set()

    while True:
        if fringe.isEmpty():
            return []

        current, path = fringe.pop()

        if current.isWin():
            return path

        current_key = key(current)

        if current_key in closed:
            continue
        else:
            closed.add(current_key)

        for successor, action in current.generatePacmanSuccessors():
            fringe.push((successor, path + [action]))

    return path

