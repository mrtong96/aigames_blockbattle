
from util import PriorityQueue
import util
from piece import Piece

# treis to get piece from start to end position

class BoardSearchProblem():
    #def __init__(self, board, start_piece, start_loc, end_piece, end_loc):
    def __init__(self, board, piece_type, start_rot, start_loc, end_rot, end_loc):
        self.board = board

        self.piece_type = piece_type
        self.start_rotations = start_rot
        self.start_loc = start_loc
        self.end_rotations = end_rot
        self.end_loc = end_loc

    def getStartState(self):
        return self.piece_type, self.start_rotations, self.start_loc

    # returns state, action pairs
    def getSuccessors(self, cur_state):
        cur_piece_type, cur_rotations, cur_loc = cur_state
        cur_piece = Piece(cur_piece_type, right_rotations=cur_rotations)
        possible_actions = ['up', 'left', 'right', 'turnleft', 'turnright']

        state_action_pairs = []

        for action in possible_actions:
            if action == 'up' or action == 'left' or action == 'right':
                if action == 'up':
                    shifted_loc = (cur_loc[0], cur_loc[1] - 1)
                elif action == 'left':
                    shifted_loc = (cur_loc[0] - 1, cur_loc[1])
                else:
                    shifted_loc = (cur_loc[0] + 1, cur_loc[1])

                piece_copy = cur_piece.copy()
                blocks = piece_copy.get_locations()
                blocks = map(lambda x: (x[0] + shifted_loc[0], x[1] + shifted_loc[1]), blocks)
            else:
                shifted_loc = cur_loc

                piece_copy = cur_piece.copy()
                if action == 'turnleft':
                    piece_copy.rotate_left()
                else:
                    piece_copy.rotate_right()
                blocks = piece_copy.get_locations()

            append = True
            for x_block, y_block in blocks:
                #if x_block < 0 or y_block < 0 or\
                if x_block < 0 or y_block < -cur_piece.size or\
                    x_block >= self.board.width or y_block >= self.board.height:
                    append = False
                    break
                elif y_block >= 0 and self.board.data[y_block][x_block] > 1:
                    append = False
                    break
            if append:
                state_action_pairs.append(((piece_copy._type, piece_copy.right_rotations, shifted_loc), action))

        return state_action_pairs


    def isGoalState(self, state):
        return self.piece_type == state[0] and self.end_rotations == state[1]\
            and self.end_loc == state[2]

    def getCostOfActions(self, actions):
        return len(actions)

def boardHeuristic(cur_state, problem):
    cur_piece_type, cur_rotations, cur_loc = cur_state
    end_loc = problem.end_loc

    total = 0

    total += abs(cur_loc[0] - end_loc[0])
    total += abs(cur_loc[1] - end_loc[1])
    rotation_difference = abs(cur_rotations - problem.end_rotations)
    # how many rotations needed to match the end_piece's rotation
    total += -abs(rotation_difference - 2) + 2

    return total

# A* search copied from cs188 project

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    closed = set([problem.getStartState()])
    fringe = util.PriorityQueue()

    for successor in problem.getSuccessors(problem.getStartState()):
        fringe.push(([successor[1]], successor[0]), problem.getCostOfActions([successor[1]])\
            + heuristic(successor[0], problem))

    while True:
        if fringe.isEmpty():
            return 'Error'
        currentPath, currentState = fringe.pop()
        if problem.isGoalState(currentState):
            return currentPath
        if currentState not in closed:
            closed.add(currentState)
            for successorState in problem.getSuccessors(currentState):
                newPath = currentPath + [successorState[1]]
                fringe.push((newPath, successorState[0]), problem.getCostOfActions(newPath)\
                    + heuristic(successorState[0], problem))

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    closed = set([problem.getStartState()])
    fringe = util.Stack()
    for successor in problem.getSuccessors(problem.getStartState()):
        fringe.push(([successor[1]], successor[0]))

    while True:
        if fringe.isEmpty():
            return 'Error'
        currentPath, currentState = fringe.pop()
        if problem.isGoalState(currentState):
            return currentPath
        if currentState not in closed:
            closed.add(currentState)
            for successorState in problem.getSuccessors(currentState):
                newPath = currentPath + [successorState[1]]
                fringe.push((newPath, successorState[0]))
                if problem.isGoalState(currentState):
                    return newPath
