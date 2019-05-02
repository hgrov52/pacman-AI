# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """

    # Actions = []
    # Visited = [problem.getStartState()]
    # return dfshelper(problem, problem.getStartState(), Actions, Visited)
    

    stack = util.Stack()
    stack.push([[problem.getStartState(),""]])
    Visited = []

    while(not stack.isEmpty()):
        path = stack.pop()
        state = path[-1][0]

        if(problem.isGoalState(state)):
            return [x[1] for x in path[1:]]

        if(state not in Visited):
            Visited.append(state)
            for successor in problem.getSuccessors(state):
                successor_state = successor[0]
                if(successor_state not in Visited):
                    stack.push(path+[[successor_state,successor[1]]])


def dfshelper(problem, state, Actions, Visited):
    if(problem.isGoalState(state)):
        return Actions

    paths = []
    for successor in problem.getSuccessors(state):
    
        state = successor[0]
        action = successor[1]
        if(state not in Visited):
            path = dfshelper(problem,state,Actions+[action],Visited+[state])
            if(path!=[]):
                paths.append(path)

    
    if(paths!=[]):
        best_path = [],99999999
        for path in paths:
            if(problem.getCostOfActions(path)<best_path[1]):
                best_path = path,problem.getCostOfActions(path)
        return best_path[0]
    return []

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    stack = util.Queue()
    stack.push([[problem.getStartState(),""]])
    Visited = []

    while(not stack.isEmpty()):
        path = stack.pop()
        state = path[-1][0]

        if(problem.isGoalState(state)):
            return [x[1] for x in path[1:]]

        if(state not in Visited):
            Visited.append(state)
            for successor in problem.getSuccessors(state):
                successor_state = successor[0]
                if(successor_state not in Visited):
                    stack.push(path+[[successor_state,successor[1]]])

def bfshelper(problem, state, Actions, Visited):
    return []

def uniformCostSearch(problem):
    function = lambda x: problem.getCostOfActions([p[1] for p in x[1:]])
    stack = util.PriorityQueueWithFunction(function)
    stack.push([[problem.getStartState(),""]])
    Visited = []

    while(not stack.isEmpty()):
        path = stack.pop()
        state = path[-1][0]

        if(problem.isGoalState(state)):
            return [x[1] for x in path[1:]]

        if(state not in Visited):
            Visited.append(state)
            for successor in problem.getSuccessors(state):
                successor_state = successor[0]
                if(successor_state not in Visited):
                    stack.push(path+[[successor_state,successor[1]]])


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    function = lambda x: problem.getCostOfActions([p[1] for p in x[1:]])+heuristic(x[-1][0],problem)
    stack = util.PriorityQueueWithFunction(function)
    stack.push([[problem.getStartState(),""]])
    Visited = []

    while(not stack.isEmpty()):
        path = stack.pop()
        state = path[-1][0]

        if(problem.isGoalState(state)):
            return [x[1] for x in path[1:]]

        if(state not in Visited):
            Visited.append(state)
            for successor in problem.getSuccessors(state):
                successor_state = successor[0]
                if(successor_state not in Visited):
                    stack.push(path+[[successor_state,successor[1]]])



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
