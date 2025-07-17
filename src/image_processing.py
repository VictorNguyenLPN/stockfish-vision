# src/image_processing.py
import cv2
import numpy as np

def process_image_from_path(file_path):
    try:
        img_bgr = cv2.imread(file_path)
        # cv2.imshow("BGR color Image", img_bgr)

        if img_bgr is None:
            print(f"ERROR: Can not read image from {file_path}")
            return None

        return _get_fen_from_image(img_bgr)
    except Exception as e:
        print(f"ERROR: Can not process image - {e}")
        return None

def _get_fen_from_image(image_bgr):
    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("1 - Grayscale Image", gray_image)
    # cv2.waitKey(0)

    edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)
    # cv2.imshow("2 - Edges Detected", edges)
    # cv2.waitKey(0)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Found total {len(contours)} contours.")
    image_with_all_contours = gray_image.copy()
    # cv2.drawContours(image_with_all_contours, contours, -1, (0, 255, 0), 2)
    # cv2.imshow("3 - All Contours Found", image_with_all_contours)
    # cv2.waitKey(0)

    board_contour = max(contours, key=cv2.contourArea)
    print(f"Detected the largest contour {cv2.contourArea(board_contour)}")
    image_with_board_contour = gray_image.copy()
    cv2.drawContours(image_with_board_contour, [board_contour], 0, (0, 255, 0), 3)
    cv2.imshow("4 - Board Contour", image_with_board_contour)
    cv2.waitKey(0)

    x, y, w, h = cv2.boundingRect(board_contour)
    board_img = image_bgr[y:y+h, x:x+w]
    board_img = image_bgr[y:y+h, x:x+w]
    print(f"Cut chessboard with size: {w}x{h}")
    # cv2.imshow("5 - Cropped Board", board_img)
    # cv2.waitKey(0)

    square_size = w // 8
    squares = []
    print(f"cut into 64 cell, each cell sized: {square_size}x{square_size}")
    for row in range(8):
        for col in range(8):
            sx = col * square_size
            sy = row * square_size
            square_img = board_img[sy:sy+square_size, sx:sx+square_size]
            squares.append(square_img)
    for i in range (20):
        cv2.imshow(f"6 - Sample Square ({i})", squares[i])
        cv2.waitKey(0)

    piece_templates = {
        'K': cv2.imread('templates/wK.png', 0),
        'Q': cv2.imread('templates/wQ.png', 0),
        'R': cv2.imread('templates/wR.png', 0),
        'B': cv2.imread('templates/wB.png', 0),
        'N': cv2.imread('templates/wN.png', 0),
        'P': cv2.imread('templates/wP.png', 0),
        'k': cv2.imread('templates/bK.png', 0),
        'q': cv2.imread('templates/bQ.png', 0),
        'r': cv2.imread('templates/bR.png', 0),
        'b': cv2.imread('templates/bB.png', 0),
        'n': cv2.imread('templates/bN.png', 0),
        'p': cv2.imread('templates/bP.png', 0),
    }

    board_state = []
    for square in squares:
        square_gray = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
        found_piece = None
        max_val = 0.90

        for piece, template in piece_templates.items():
            if template is None:
                # print("Template is None")
                continue

            res = cv2.matchTemplate(square_gray, template, cv2.TM_CCOEFF_NORMED)
            # print(f"res: {res}")
            min_val, curr_max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if curr_max_val > max_val:
                found_piece = piece
                print(piece)
                max_val = curr_max_val

        board_state.append(found_piece if found_piece else '')

    fen_rows = []
    for i in range(8):
        row = board_state[i*8:(i+1)*8]
        fen_row = ''
        empty_count = 0
        for cell in row:
            if cell == '':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)
    fen_string = '/'.join(fen_rows) + ' w KQkq - 0 1'

    print(f"Completed -> FEN: {fen_string}")

    # sample = "rn2kbnr/1ppb1pp1/p7/5P2/3P3q/4P3/PPP4P/RNB1K1NR w KQkq - 1 12"
    return fen_string