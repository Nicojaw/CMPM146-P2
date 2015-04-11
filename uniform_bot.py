from random import randint

def think(state, quip):
  moves = state.get_moves()
  Lmov = len (moves)
  return state.get_moves()[randint(0, Lmov-1)]