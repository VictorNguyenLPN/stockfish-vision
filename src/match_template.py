#  src/match_template.py

import cv2
import os
import numpy as np
from src.logger import get_logger

logger = get_logger(__name__)

TEMPLATE_DIR = "templates"
LABEL_ORDER = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN', 'bP', 'empty']

def __remove_transparent_border(image: str):
    b, g, r, a = cv2.split(image)
    alpha_mask = a > 0

    coords = np.argwhere(alpha_mask)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1

    cropped = image[y0:y1, x0:x1]
    bgr_cropped = cv2.cvtColor(cropped, cv2.COLOR_BGRA2BGR)

    return bgr_cropped

def __load_image(image_path: str, window_name: str = "BGR image"):
    try:
        image = cv2.imread(filename=image_path, flags=cv2.IMREAD_UNCHANGED)
        if image is None:
            logger.error(f"Image is none")
            return None

        if image.shape[2] == 4:
            bgr_image_cropped = __remove_transparent_border(image=image)

            if window_name:
                cv2.imshow(winname=window_name, mat=bgr_image_cropped)
                cv2.waitKey(0)

            return bgr_image_cropped

    except Exception as e:
        logger.error(f"Can't get image from {image_path}: {e}")
        return None

def __load_templates(verbose: bool = False):
    piece_templates = {'light': {}, 'dark': {}}

    for filename in os.listdir(TEMPLATE_DIR):
        if filename.endswith(".png"):
            parts = filename.replace(".png", "").split('_')
            if len(parts) != 2:
                continue

            piece_label, piece_variant_id = parts
            variant = 'light' if piece_variant_id == '1' else 'dark'

            path = os.path.join(TEMPLATE_DIR, filename)
            piece_template = __load_image(image_path=path, window_name=None)
            piece_template_gray = cv2.cvtColor(piece_template, cv2.COLOR_BGR2GRAY)
            piece_templates[variant][piece_label] = piece_template_gray

            if verbose:
                cv2.imshow(f"{variant}-{piece_label}", piece_template_gray)
                cv2.waitKey(0)

    return piece_templates

def __classify_cell(selected_cell, piece_templates, square_type, threshold=0.5):
    best_score = -1
    best_label = "empty"

    selected_cell_gray = cv2.cvtColor(selected_cell, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(0)
    for piece_label, piece_template in piece_templates[square_type].items():
        resize_piece_template = cv2.resize(piece_template, (90, 90))
        res = cv2.matchTemplate(resize_piece_template, selected_cell_gray, cv2.TM_CCOEFF_NORMED)
        score = np.max(res)
        if score > best_score:
            best_score = score
            best_label = piece_label

    # logger.debug(f"[{square_type}] {best_label} - {best_score:.3f}")

    if best_score >= threshold:
        return best_label
    return "empty"

def __label_to_fen_symbol(label: str) -> str:
    if label == "empty":
        return ""
    piece = label[1]
    is_white = label[0] == "w"
    return piece.upper() if is_white else piece.lower()

def __compress_fen_row(row_symbols: list) -> str:
    compressed = ""
    empty_count = 0
    for s in row_symbols:
        if s == "":
            empty_count += 1
        else:
            if empty_count > 0:
                compressed += str(empty_count)
                empty_count = 0
            compressed += s
    if empty_count > 0:
        compressed += str(empty_count)
    return compressed

def generate_fen_from_image(image_path: str):
    logger.info(f"1. Processing image from {image_path}")

    bgr_image = __load_image(image_path=image_path, window_name=None)
    if bgr_image is None:
        logger.error("Image is None")
        return None

    bgr_image_copy = bgr_image.copy()
    h, w = bgr_image_copy.shape[:2]
    cell_size = w //8
    logger.info(f"2. Board's shape: {bgr_image_copy.shape[0]}x{bgr_image_copy.shape[1]}\n\t\t\t\tCut into 8 cell: {bgr_image_copy.shape[0]//8}x{bgr_image_copy.shape[1]//8}")

    templates = __load_templates(verbose=False)

    logger.info(f"3. Matching template")
    board_labels = []
    for row in range(8):
        row_labels = []
        for col in range(8):
            sx = col * cell_size
            sy = row * cell_size
            selected_cell = bgr_image_copy[sy:sy+cell_size, sx:sx+cell_size]

            square_type = 'light' if (row + col) % 2 == 0 else 'dark'
            label = __classify_cell(selected_cell, templates, square_type)
            row_labels.append(__label_to_fen_symbol(label))
        board_labels.append(row_labels)

    fen_rows = [__compress_fen_row(row) for row in board_labels]
    fen = "/".join(fen_rows)
    logger.info(f"4. FEN: {fen}")

    print("-"*33)
    for row in board_labels:
        print("|"," | ".join(s if s else "." for s in row), "|")
        print("-"*33)
    return fen