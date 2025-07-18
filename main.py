# stockfish-vision/main.py

from src.image_processing import process_image_from_path

fen = process_image_from_path("images/screenshot.png")
print("FEN Result:", fen)