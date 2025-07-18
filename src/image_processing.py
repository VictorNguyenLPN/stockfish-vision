# stockfish-vision/src/image_processing.py

import cv2
import numpy as np
from torchvision import transforms
from PIL import Image
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load('models/cnn_chess_piece.pt', weights_only=False)
model.eval()

transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((100, 100)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

index_to_fen = {
    0: 'bB', 1: 'bK', 2: 'bN', 3: 'bP', 4: 'bQ', 5: 'bR',
    6: 'wB', 7: 'wK', 8: 'wN', 9: 'wP', 10: 'wQ', 11: 'wR',
    12: ''  # empty square
}

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
    # image_with_all_contours = gray_image.copy()
    # cv2.drawContours(image_with_all_contours, contours, -1, (0, 255, 0), 2)
    # cv2.imshow("3 - All Contours Found", image_with_all_contours)
    # cv2.waitKey(0)

    board_contour = max(contours, key=cv2.contourArea)
    print(f"Detected the largest contour {cv2.contourArea(board_contour)}")
    # image_with_board_contour = gray_image.copy()
    # cv2.drawContours(image_with_board_contour, [board_contour], 0, (0, 255, 0), 3)
    # cv2.imshow("4 - Board Contour", image_with_board_contour)
    # cv2.waitKey(0)

    x, y, w, h = cv2.boundingRect(board_contour)
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
    # for i in range (20):
    #     cv2.imshow(f"6 - Sample Square ({i})", squares[i])
    #     cv2.waitKey(0)

    board_state = []
    for square in squares:
        img_pil = Image.fromarray(cv2.cvtColor(square, cv2.COLOR_BGR2RGB))
        img_tensor = transform(img_pil).unsqueeze(0).to(device)
        with torch.no_grad():
            output = model(img_tensor)
            probs = torch.softmax(output, dim=1)
            pred_idx = probs.argmax(1).item()
            confidence = probs[0][pred_idx].item()

            if pred_idx == 12 or confidence < 0.70:
                board_state.append('')
            else:
                found_piece = index_to_fen[pred_idx]
                board_state.append(found_piece)

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

    # sample = "r2qkbnr/ppp2ppp/2n5/3pp3/2B1P1b1/5N2/PPPP1PPP/RNB1K2R w KQkq - 0 5"
    return fen_string

def center_crop(image, size):
    h, w = image.shape
    startx = w//2 - size//2
    starty = h//2 - size//2
    return image[starty:starty+size, startx:startx+size]