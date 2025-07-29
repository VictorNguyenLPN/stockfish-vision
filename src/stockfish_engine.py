from stockfish import Stockfish

def suggest(position : str):
    stockfish = Stockfish(path="/usr/games/stockfish")
    stockfish.set_depth(30)
    stockfish.set_fen_position(position)
    best_move = stockfish.get_best_move()

    return best_move