import cv2
import numpy as np

def get_color(image, c):
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mean_hsv = cv2.mean(hsv, mask=mask)[:3]
    mean_hsv = np.array(mean_hsv, dtype=np.float32)
    color_refs = {
        "Red":   np.array([  0, 180, 200], dtype=np.float32),
        "Orange":np.array([ 12, 180, 200], dtype=np.float32),
        "Yellow":np.array([ 30, 180, 200], dtype=np.float32),
        "Green": np.array([ 60, 180, 200], dtype=np.float32),
        "Blue":  np.array([110, 180, 200], dtype=np.float32),
        "Purple":np.array([140, 150, 180], dtype=np.float32),
        "Pink":  np.array([160, 150, 200], dtype=np.float32),
        "Gray":  np.array([  0,  20, 120], dtype=np.float32),
        "Brown": np.array([ 10, 150, 120], dtype=np.float32)
    }

    color_name = None
    min = float("inf")
    for name, ref in color_refs.items():
        d = np.linalg.norm(mean_hsv - ref)
        if d < min:
            min = d
            color_name = name

    return color_name