from random import randint

def think(state, quip):
  moves = state.get_moves()
  Lmov = len (moves)
  prev = state.get_score()[state.get_whos_turn()]
  quip(state.get_score())
  
  for m in moves:
    cpy = state.copy()
    cpy.apply_move(m)
    if cpy.get_score()[state.get_whos_turn()] > prev:
      return m 
	
  return state.get_moves()[randint(0, Lmov-1)]