# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.
        getAction chooses among the current_best options according to the evaluation function.
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the current_best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        current_bestScore = max(scores)
        current_bestIndices = [index for index in range(len(scores)) if scores[index] == current_bestScore]
        chosenIndex = random.choice(current_bestIndices) # Pick randomly among the current_best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        return_value = successorGameState.getScore()

        ghost_dists = []
        for g in newGhostStates:
          ghost_dists.append(manhattanDistance(newPos,g.getPosition()))

        if(len(ghost_dists)!=0 and min(ghost_dists)!=0):
          return_value -= 10 / min(ghost_dists)

        food_dists = []
        for f in newFood.asList():
          food_dists.append(manhattanDistance(newPos,f))

        if(len(food_dists)!=0):
          return_value += 10 / min(food_dists)

        return return_value

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.
      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.
      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def expand_tree(state,depth,num_agents):
          if(num_agents != state.getNumAgents()):
            next_actions = state.getLegalActions(num_agents)
            if(len(next_actions)==0):
              return self.evaluationFunction(state)
            next_states = []
            for action in next_actions:
              next_states.append(expand_tree(state.generateSuccessor(num_agents,action),depth,num_agents+1))
            if(num_agents == 0):
              return max(next_states)
            return min(next_states)
          if(depth == self.depth):
            return self.evaluationFunction(state)
          return expand_tree(state,depth+1,0)
        
        _max = -999999
        index = 0;
        for a_index in range(len(gameState.getLegalActions(0))):
          action = gameState.getLegalActions(0)[a_index]
          nextState = gameState.generateSuccessor(0,action)  
          value = expand_tree(nextState,1,1)
          if(value >_max):
            _max = value
            index = a_index

        return gameState.getLegalActions(0)[index]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"



        def minmax_player(state, depth, num_agents, Alpha, Beta, mm=True):
          if (num_agents == state.getNumAgents()):
            if(depth == self.depth):
              return self.evaluationFunction(state)
            else:
              return minmax_player(state, depth+1, 0, Alpha, Beta,False)
          #=======================
          # same for min/max player except Alpha/Beta - using mm
          current_value = None
          for action in state.getLegalActions(num_agents):
            nextState = state.generateSuccessor(num_agents,action)
            if(mm):
              successor = minmax_player(nextState, depth, num_agents+1, Alpha, Beta)
              if(current_value == None or successor<current_value):
                current_value = successor
              if(Alpha != None and Alpha > current_value):
                # prune
                return current_value
              if(current_value!=None and (Beta == None or current_value < Beta)):
                Beta = current_value

            else:
              successor = minmax_player(nextState, depth, num_agents+1, Alpha, Beta)
              if(successor>current_value):
                current_value = successor
              if(Beta != None and Beta < current_value):
                # prune
                return current_value
              if(Alpha < current_value):
                Alpha = current_value

          if current_value is None:
            return self.evaluationFunction(state)

          return current_value

        current_value = -999999
        Alpha = None
        Beta = None
        current_best = -999999

        for action in gameState.getLegalActions(0):
          nextState = gameState.generateSuccessor(0,action)
          current_value = max(current_value, minmax_player(nextState, 1, 1, Alpha, Beta))
          if(Alpha == None or current_value > Alpha):
            Alpha, current_best = current_value, action
          
        return current_best


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(state, depth, num_agents):
            if num_agents == state.getNumAgents():
              if depth == self.depth:
                return self.evaluationFunction(state)
              else:
                return expectimax(state, depth+1, 0)

            successor_states = []
            for action in state.getLegalActions(num_agents):
              nextState = state.generateSuccessor(num_agents,action)
              successor_states.append(expectimax(nextState,depth,num_agents+1))

            if(successor_states == []):
              return self.evaluationFunction(state)

            if(num_agents==0):
              return max(successor_states)
            else:
              return sum(successor_states)/len(successor_states)

        _max = -999999
        index = 0;
        for a_index in range(len(gameState.getLegalActions(0))):
          action = gameState.getLegalActions(0)[a_index]
          nextState = gameState.generateSuccessor(0,action)  
          value = expectimax(nextState,1,1)
          if(value >_max):
            _max = value
            index = a_index

        return gameState.getLegalActions(0)[index]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: my implementation is similar to what I did for
      the original evaluation function except that I now take into 
      consideration the ghosts when they are able to be eaten for 
      extra points, where that is less of a priority but still 
      important. The other major change is that fact that the return
      value considers every ghost position rather than the closest one.
      It still only considers the closest food, the same as the earlier
      evaluation function. 
    """
    "*** YOUR CODE HERE ***"
    # taken from the given part of the original eval function
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return_value = currentGameState.getScore()

    for g in newGhostStates:
      d = manhattanDistance(newPos, newGhostStates[0].getPosition())
      if d > 0:
        # if the ghost is edible or not
        if g.scaredTimer != 0:  
          # go towards a ghost bc he is edible
          return_value += 50 / d
        else: 
          # run from a ghost bc he isnt edible
          return_value -= 10 / d

    min_food_dist = 999999
    for f in newFood.asList():
      d = manhattanDistance(newPos,f)
      if(d < min_food_dist):
        min_food_dist = d
    
    return_value += 10 / min_food_dist

    return return_value

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.
          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
