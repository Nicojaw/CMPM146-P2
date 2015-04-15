from random import randint

def think(state, quip):
  moves = state.get_moves()
  Lmov = len (moves)
  prev = state.get_score()[state.get_whos_turn()]
  quip(state.get_score())
  best = 0
  bestMove = None
  
  for m in moves:
    cpy = state.copy()
    cpy.apply_move(m)
    if cpy.get_score()[state.get_whos_turn()] >= best:
      best = cpy.get_score()[state.get_whos_turn()]
      bestMove = m 
	
  return bestMove