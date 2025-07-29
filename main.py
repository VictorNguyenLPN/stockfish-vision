from src.match_template import generate_fen_from_image
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nhận diện bàn cờ từ ảnh và sinh FEN.")

    parser.add_argument(
        "--image", "-i",
        type=str,
        required=True,
        help="Đường dẫn tới ảnh bàn cờ (ví dụ: ./images/board_3.png)"
    )

    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Bật chế độ debug (in thêm thông tin trung gian)"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Ghi FEN ra file (tuỳ chọn)"
    )

    args = parser.parse_args()

    fen = generate_fen_from_image(args.image, debug=args.debug)

    print("FEN:", fen)

    if args.output:
        with open(args.output, "w") as f:
            f.write(fen)
        print(f"Đã ghi FEN vào: {args.output}")


"""
TEST CASE
    board_1 (initial chessboard):rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
    board_2: R2KQBNR/PPP1PPPP/2N5/3P4/3p4/2q2B2/ppp1pppp/rnbk1bnr
    board_3: 5BNR/2PKPPPP/1P6/3P2b1/R7/2n2p1n/ppp1kppp/r6r
"""