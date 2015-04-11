from random import choice
from math import *
import time

class Node:
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.score = 0
        self.visits = 0
        self.untriedMoves = state.get_moves() # future child nodes
        self.player = state.get_whos_turn() # the only part of the state that the Node needs later
        
    def RewardFunc(self,Gstate,state):
        reWar = 0
        if Gstate.get_score()['blue'] == Gstate.get_score()[state.get_whos_turn()]:
          print str(Gstate.get_score())
          reWar = Gstate.get_score()['blue'] - Gstate.get_score()['red']
        else:
          reWar = Gstate.get_score()['red'] - Gstate.get_score()['blue']    
        return reWar
        
    def UCTSelectChild(self,res):   
        s = sorted(self.childNodes, key = lambda c: res + sqrt(log(self.visits)/c.visits))[-1]
        return s
    
    def AddChild(self, m, s):
          # Remove m from untriedMoves and add a new child node for this move.
          # Return the added child node
        
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):# Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        self.visits += 1
        self.score += result
        

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s

def think(state, quip):
  moves = state.get_moves()
  Lmov = len (moves)
  prev = state.get_score()[state.get_whos_turn()]
  
  """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

  rootnode = Node(state = state)
  
  timeNow = int(round(time.time()))

  while int(round(time.time())) - timeNow < 1:
      node = rootnode
      gamestate = state.copy()

      # Select
      while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
          res = node.RewardFunc(gamestate,state)
          node = node.UCTSelectChild(res)
          gamestate.apply_move(node.move)

      # Expand
      if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
          m = choice(node.untriedMoves) 
          gamestate.apply_move(m)
          node = node.AddChild(m,gamestate) # add child and descend tree

      # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
      while gamestate.get_moves() != []: # while state is non-terminal
          gamestate.apply_move(choice(gamestate.get_moves()))
       # Backpropagate
      while node != None: # backpropagate from the expanded node and work back to the root node
          node.Update(state.get_score()[state.get_whos_turn()]) # state is terminal. Update node with result from POV of node.playerJustMoved
          node = node.parentNode
  
  selected = sorted(rootnode.childNodes, key = lambda c: c.visits)[-1]
  print "selected score: " + str(selected.score)
  return selected.move # return the move that was most visited   