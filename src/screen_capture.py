import mss
import numpy as np
import cv2

def capture_screen(region=None):
    # region = {"top": 208, "left": 250, "width": 930, "height": 930}

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        if region is None:
            region = monitor

        screenshot = sct.grab(region)
        img = np.array(screenshot)

        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

# if __name__ == "__main__":
#     region = {"top": 208, "left": 250, "width": 930, "height": 930}
#     while True:
#         frame = capture_screen(region)
#         cv2.imshow("Live Screen", frame)

#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break

#     cv2.destroyAllWindows()