# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




from dataclasses import dataclass
from typing import Optional
@dataclass(frozen=True)
class Node:
    """
    Define a Data Class to store nodes information
    state: the state of node e.g. (12,24)
    pred: from which node to current node
    action: what action to take to get this node 
    priority: use for UCS
    """
    state: tuple
    pred: Optional['Node'] = None
    action: str = None
    priority: int = 1
    
    def __str__(self):
        return f"State: {self.state}, Action: {self.action}"


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    # print("Start:", problem.getStartState()) #  (34, 16)
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState())) # False
    # print("Start's successors:", problem.getSuccessors(problem.getStartState())) # ((34, 15), 'South', 1)
    closed = set()
    fringe = util.Stack()
    fringe.push(Node(problem.getStartState(),None, None))
    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state):
            actions = []
            while node.action is not None:
                actions.append(node.action)
                node = node.pred
            actions.reverse()
            return actions

        if node.state not in closed:
            closed.add(node.state)
            for s in problem.getSuccessors(node.state):
                fringe.push(Node(s[0], node, s[1]))
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    closed = set()
    fringe = util.Queue()
    fringe.push(Node(problem.getStartState(), None, None))
    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state):
            actions = []
            while node.action is not None:
                actions.append(node.action)
                node = node.pred
            actions.reverse()
            return actions

        if node.state not in closed:
            closed.add(node.state)
            for s in problem.getSuccessors(node.state):
                fringe.push(Node(s[0], node, s[1]))
    return []
            
def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    closed = set()
    fringe = util.PriorityQueue()
    fringe.push(Node(problem.getStartState(), None, None), 0)
    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state):
            actions = []
            while node.action is not None:
                actions.append(node.action)
                node = node.pred
            actions.reverse()
            return actions
        
        if node.state not in closed:
            closed.add(node.state)
            for s in problem.getSuccessors(node.state):
                fringe.push(Node(s[0], node, s[1], s[2] + node.priority), s[2] + node.priority)
    return []
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    closed = set()
    fringe = util.PriorityQueue()
    start_state = problem.getStartState()
    fringe.push(
        Node(start_state, None, None, heuristic(start_state, problem)), heuristic(start_state, problem)
    )
    
    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state):
            actions = []
            while node.action is not None:
                actions.append(node.action)
                node = node.pred
            actions.reverse()
            return actions
        
        if node.state not in closed:
            closed.add(node.state)
            for s in problem.getSuccessors(node.state):
                fringe.push(
                    Node(s[0], node, s[1], s[2] + node.priority), 
                    s[2] + node.priority + heuristic(s[0], problem)
                )
    return []
# Abbreviations 
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
