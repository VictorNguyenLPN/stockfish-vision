from src.match_template import generate_fen_from_image


if __name__ == "__main__":
    fen = generate_fen_from_image("./images/board_3.png")


"""
TEST CASE
    board_1 (initial chessboard):rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
    board_2: R2KQBNR/PPP1PPPP/2N5/3P4/3p4/2q2B2/ppp1pppp/rnbk1bnr
    board_3: 5BNR/2PKPPPP/1P6/3P2b1/R7/2n2p1n/ppp1kppp/r6r
"""