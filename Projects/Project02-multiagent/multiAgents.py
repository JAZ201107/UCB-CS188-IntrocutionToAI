# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions() 

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        nearestGhostDis = 1e9
        for ghostState in newGhostStates:
            ghostX, ghostY = ghostState.getPosition()
            ghostX = int(ghostX)
            ghostY = int(ghostY)
            if ghostState.scaredTimer == 0:
                nearestGhostDis = min(nearestGhostDis, manhattanDistance((ghostX, ghostY), newPos))
                
        nearestFootDis = 1e9
        for food in newFood.asList():
            nearestFootDis = min(nearestFootDis, manhattanDistance(food, newPos))
        if not newFood.asList():
            nearestFootDis = 0
        
        return successorGameState.getScore() - 7 / (nearestGhostDis + 1) - nearestFootDis / 3

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        return self.minimaxSearch(gameState, agentIndex=0, depth=self.depth)[1]
    
    
    def minimaxSearch(self, gameState, agentIndex, depth):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            ret = self.evaluationFunction(gameState), Directions.STOP
        elif agentIndex == 0: # for agent one
            ret = self.maximizer(gameState, agentIndex, depth)
        else:
            ret = self.minimizer(gameState, agentIndex, depth)
        return ret
    
    def minimizer(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            next_agent, next_depth = 0, depth - 1
        else:
            next_agent, next_depth = agentIndex + 1, depth
        min_score = 1e9
        min_action = Directions.STOP
        for action in actions:
            successor_game_state = gameState.generateSuccessor(agentIndex, action)
            new_score = self.minimaxSearch(successor_game_state, next_agent, next_depth)[0]
            if new_score < min_score:
                min_score, min_action = new_score, action
        return min_score, min_action

    
    def maximizer(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            next_agent, next_depth = 0, depth - 1
        else:
            next_agent, next_depth = agentIndex + 1, depth
        max_score = -1e9
        max_action = Directions.STOP
        
        for action in actions:
            successor_game_state = gameState.generateSuccessor(agentIndex, action)
            new_score = self.minimaxSearch(successor_game_state, next_agent, next_depth)[0]
            if new_score > max_score:
                max_score, max_action = new_score, action
        return max_score, max_action
            
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        return self.alphabetaSearch(gameState, 0, self.depth, -1e9, 1e9)[1]
    
    def alphabetaSearch(self, gameState, agentIndex, depth, alpha, beta):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            ret = self.evaluationFunction(gameState), Directions.STOP
        elif agentIndex == 0:
            ret = self.alphaSearch(gameState, agentIndex, depth, alpha, beta)
        else:
            ret = self.betaSearch(gameState, agentIndex, depth, alpha, beta)
        return ret 

    def alphaSearch(self, gameState, agentIndex, depth, alpha, beta):
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            next_agent, next_depth = 0, depth - 1
        else:
            next_agent, next_depth = agentIndex + 1, depth
        max_score, max_action = -1e9, Directions.STOP
        for action in actions:
            successor_game_state = gameState.generateSuccessor(agentIndex, action)
            new_score = self.alphabetaSearch(successor_game_state, next_agent, next_depth, alpha, beta)[0]
            
            if new_score > max_score:
                max_score, max_action = new_score, action
            if new_score > beta:
                return new_score, action
            alpha = max(alpha, max_score)
        return max_score, max_action

    def betaSearch(self, gameState, agentIndex, depth, alpha, beta):
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            next_agent, next_depth = 0, depth - 1
        else:
            next_agent, next_depth = agentIndex + 1, depth
        min_score, min_action = 1e9, Directions.STOP
        for action in actions:
            successor_game_state = gameState.generateSuccessor(agentIndex, action)
            new_score = self.alphabetaSearch(successor_game_state, next_agent, next_depth, alpha, beta)[0]
            if new_score < min_score:
                min_score, min_action = new_score, action
            if new_score < alpha:
                return new_score, action
            beta = min(beta, min_score)
        return min_score, min_action
    
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        return self.expectimaxsearch(gameState, 0, self.depth)[1]
    
    def expectimaxsearch(self, game_state, agent_index, depth):
        if depth == 0 or game_state.isWin() or game_state.isLose():
            ret = self.evaluationFunction(game_state), Directions.STOP
        elif agent_index == 0:
            ret = self.maximizer(game_state, agent_index, depth)
        else:
            ret = self.expectation(game_state, agent_index, depth)
        return ret

    def maximizer(self, game_state, agent_index, depth):
        actions = game_state.getLegalActions(agent_index)
        if agent_index == game_state.getNumAgents() - 1:
            next_agent, next_depth = 0, depth - 1
        else:
            next_agent, next_depth = agent_index + 1, depth
        max_score, max_action = -1e9, Directions.STOP
        for action in actions:
            successor_game_state = game_state.generateSuccessor(agent_index, action)
            new_score = self.expectimaxsearch(successor_game_state, next_agent, next_depth)[0]
            if new_score > max_score:
                max_score, max_action = new_score, action
        return max_score, max_action

    def expectation(self, game_state, agent_index, depth):
        actions = game_state.getLegalActions(agent_index)
        if agent_index == game_state.getNumAgents() - 1:
            next_agent, next_depth = 0, depth - 1
        else:
            next_agent, next_depth = agent_index + 1, depth
        exp_score, exp_action = 0, Directions.STOP
        for action in actions:
            successor_game_state = game_state.generateSuccessor(agent_index, action)
            exp_score += self.expectimaxsearch(successor_game_state, next_agent, next_depth)[0]
        exp_score /= len(actions)
        return exp_score, exp_action # exp_action is never used!

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    pacman_pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    foods = food.asList()
    ghost_states = currentGameState.getGhostStates()
    scared_times = [ghost_state.scaredTimer for ghost_state in ghost_states]

    nearest_ghost_dis = 1e9
    for ghost_state in ghost_states:
        ghost_x, ghost_y = ghost_state.getPosition()
        ghost_x = int(ghost_x)
        ghost_y = int(ghost_y)
        if ghost_state.scaredTimer == 0:
            nearest_ghost_dis = min(nearest_ghost_dis,\
                                    manhattanDistance((ghost_x, ghost_y),\
                                    pacman_pos))
        else:
            nearest_ghost_dis = -10
    nearest_food_dis = 1e9
    for food in foods:
        nearest_food_dis = min(nearest_food_dis,manhattanDistance(food, pacman_pos))
    if not foods:
        nearest_food_dis = 0
    return currentGameState.getScore()-7/(nearest_ghost_dis+1)\
           -nearest_food_dis/3

# Abbreviation
better = betterEvaluationFunction
