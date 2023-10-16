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
    from util import Stack
    stack=Stack() #υλοποιείται στο util.h με λίστα
    path=[] 
    visited=[]
    currnode=problem.getStartState()
    if (problem.isGoalState(currnode)==True):
        return path[1]   #maybe the first node we've been provided is the goal
    stack.push((currnode,[])) #there is no path for the first node (the root) 
    while stack: #while stack is not empty
        #starting of the backtrack^^
        currnode,path=stack.pop() #το stack έχει tuple, συνεπώς οι συντεταγμένες(χ,ψ) του κομβου θα πάνε στο currnode και το path κινήσεων θα πάει στο path
        visited.append(currnode) #αποθηκεύουμε το visited κομβο, ώστε αργότερα στην επανάληψη να προσπελάσουμε τον κόμβο στον οποίο δεν μπήκαμε τη προηγούμενη φορά.
        if problem.isGoalState(currnode)==1:
                    return path
        next_node=problem.getSuccessors(currnode)
        for node in next_node: #το next_node είναι λίστα με tuples. Το node[0] είναι οι συντεταγμένες
            if node[0] not in visited:
                new_path=path+[node[1]]
                stack.push((node[0],new_path))

       
    


    

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    queue=Queue()
    visited=set() #a list to mark which queue we have visited
    path=[] #a list with the actions the pac man needs to follow in order to find the goal
    currnode=problem.getStartState()
    visited.add(currnode)
    queue.push((currnode,[])) #list with tuple
    while queue.isEmpty()==0: #while "queue" is not empty
        currnode,path=queue.pop()
        if problem.isGoalState(currnode)==1:
            return path
        neighbor_node=problem.getSuccessors(currnode)
        for next_nodes in neighbor_node:
            if next_nodes[0] not in visited:
                new_path=path+[next_nodes[1]]
                queue.push((next_nodes[0],new_path))
                visited.add(next_nodes[0])
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    pqueue=PriorityQueue() #pqueue is gonna save the xy and the path as a tuple and the minimum distance (maximum priority)
    visited=set() #a list that saves which node we have already visited
    currnode= problem.getStartState()
    neighbor_nodes=set()
    path=[] #initializing path as an empty list
    pqueue.push((currnode,[]),0) #there is no path at the start

    while pqueue: #while the graph still has nodes
        old_distance=0
        currnode,path=pqueue.pop()
        if problem.isGoalState(currnode)==1:
            return path
        if currnode not in visited:
            visited.add(currnode)
        neighbor_nodes=problem.getSuccessors(currnode)
            
        for next_node in neighbor_nodes:
            if next_node[0] not in visited and not any(next_node[0]==node[2][0] for node in pqueue.heap): #Σημαντική επεξήγση: Στο utils.h το heappush είναι της μορφής (priority, self.count, item)
                new_path=path+[next_node[1]]                                                              #Συνεπώς το node[2][0] επιστρέφει το χψ, και το node[2][1] το new_path που κάνουμε push.  
                distance=problem.getCostOfActions(new_path)                                               #Η διαδικασία κατανόησης, ΔΕΝ είχε πλάκα!!
                pqueue.push((next_node[0],new_path),distance)
            if next_node[0] not in visited and  any(next_node[0]==node[2][0] for node in pqueue.heap):
                for node in pqueue.heap:
                    if node[2][0]==next_node[0]:
                        old_distance=problem.getCostOfActions(node[2][1])
                new_distance=problem.getCostOfActions(path+[next_node[1]])


                if new_distance<old_distance:
                    new_path=path+[next_node[1]]
                    pqueue.update((next_node[0],new_path),distance)
           

            
            
            
            

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
