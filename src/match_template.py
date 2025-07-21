#  src/match_template.py

import cv2
import os
import numpy as np
from src.logger import get_logger

logger = get_logger(__name__)

TEMPLATE_DIR = "templates"
LABEL_ORDER = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN', 'bP', 'empty']

def __load_image(image_path: str, window_name: str = "BGR image"):
    try:
        image = cv2.imread(filename=image_path, flags=cv2.IMREAD_UNCHANGED)
        if image is None:
            logger.error(f"Image is none")
            return None

        if image.shape[2] == 4:
            b, g, r, a = cv2.split(image)
            alpha_mask = a > 0

            coords = np.argwhere(alpha_mask)
            y0, x0 = coords.min(axis=0)
            y1, x1 = coords.max(axis=0) + 1

            cropped = image[y0:y1, x0:x1]
            bgr_cropped = cv2.cvtColor(cropped, cv2.COLOR_BGRA2BGR)

            if window_name:
                cv2.imshow(winname=window_name, mat=bgr_cropped)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            logger.info(f"Loaded image success. Shape: {bgr_cropped.shape}")
            return bgr_cropped

    except Exception as e:
        logger.error(f"Can't get image from {image_path}: {e}")
        return None