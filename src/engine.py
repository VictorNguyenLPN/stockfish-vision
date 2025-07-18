# src/engine.py

import chess
import chess.engine
import os

STOCKFISH_PATH = os.path.join(os.path.dirname(__file__), "stockfish")

def get_best_move(fen_string):
    if not os.path.exists(STOCKFISH_PATH):
        return "ERROR: not found stockfish at " + STOCKFISH_PATH

    try:
        if not os.access(STOCKFISH_PATH, os.X_OK):
             os.chmod(STOCKFISH_PATH, 0o755)

        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        board = chess.Board(fen_string)

        result = engine.play(board, chess.engine.Limit(time=1.0))
        engine.quit()

        return str(result.move)

    except Exception as e:
        return f"Engine error: {e}"