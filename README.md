# 🎨 Shape, Color & Centroid Detection (OpenCV + Python)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green.svg)](https://opencv.org/)
[![Imutils](https://img.shields.io/badge/imutils-Contours-lightgrey.svg)](https://pypi.org/project/imutils/)

Detects **shapes**, identifies their **colors**, computes the **centroid (x, y)** of each shape, and overlays the results on the image. Prints a neat console summary for each detection.

---

## ✨ Features

* 🟩 Contour-based **shape detection**
* 🎨 **Color** identification per shape region
* 🎯 **Centroid** computation using image moments
* 🖼️ On-image annotations + 🖨️ console logs

---

## 📂 Project Structure

```
├── main.py                # Entry point (CLI)
├── shapedetector.py       # Shape detection utilities (detect)
├── centre_of_shape.py     # Centroid utilities (findCentroid)
├── color_detector.py      # Color extraction utilities (get_color)
└── README.md              # This file
```

---

## ⚙️ Installation & Requirements

> 📝 **Note:** The table below uses **Markdown table syntax**, **not YAML**. It may *look* similar to YAML because of its structured layout.

| Dependency | Version / Command           |
| ---------- | --------------------------- |
| Python     | 3.8+                        |
| OpenCV     | `pip install opencv-python` |
| imutils    | `pip install imutils`       |

Install everything at once:

```bash
pip install opencv-python imutils
```

Optional (recommended) virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

---

## ▶️ Usage

Run the program with an input image path:

```bash
python main.py -i path/to/image.png
```

### CLI Arguments

* `-i, --image` **(required)**: Path to the input image file.

### What you’ll see

* A window titled **“Image”** that updates after each detection.
* Console output per shape like:

```
1. red triangle at (120, 85)
2. blue square at (200, 210)
3. green circle at (300, 400)
```

> 🔑 **Tip:** The code calls `cv2.waitKey(0)` inside the detection loop, so **press any key** to advance to the next detection. Press **Esc** to close.

---

## 🧠 How It Works (Pipeline)

1. **Preprocess**: Convert to grayscale → Gaussian blur → binary threshold.
2. **Contour Extraction**: `cv2.findContours(..., RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)` → `imutils.grab_contours`.
3. **Per-Contour Features**:

   * **Centroid** via `findCentroid(contour)` from `centre_of_shape.py` (moments-based).
   * **Shape** via `detect(contour)` from `shapedetector.py` (polygon approximation).
   * **Color** via `get_color(image, contour)` from `color_detector.py` (region color).
4. **Annotate**: Draw contour in green, place text label `"<color> <shape>"` at `(cX, cY)` and show the updated image.

---

## 🧩 Module Contracts (What each file should expose)

* **`shapedetector.py`**

  ```python
  def detect(contour) -> str:  # e.g., "triangle", "square", "circle"
      ...
  ```
* **`centre_of_shape.py`**

  ```python
  def findCentroid(contour) -> tuple[int, int]:  # returns (cX, cY)
      ...
  ```
* **`color_detector.py`**

  ```python
  def get_color(image, contour) -> str:  # e.g., "red", "blue", "green"
      ...
  ```

---

## 📸 Example Workflow

**Input**
*(Place an image at `docs/input.png` and link it here)*

**Output (annotated)**
*(Place an image at `docs/annotated.png` and link it here)*

```markdown
![Input](docs/input.png)
![Annotated Output](docs/annotated.png)
```

---

## ✨ Demo

```bash
python main.py -i shapes.png
```

* Console lists: `"<color> <shape> at (cX, cY)"` per object.
* OpenCV window shows contours + labels.

---

## 🧪 Sample `main.py` (Reference)

```python
from shapedetector import *
from centre_of_shape import *
from color_detector import *
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True, help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

sno = 1
for c in cnts:
    cX, cY = findCentroid(c)
    shape = detect(c)
    color = get_color(image, c)
    color_shape = f"{color} {shape}"
    print(f"{sno}. {color_shape} at ({cX},{cY})")
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, color_shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow("Image", image)
    sno += 1
    cv2.waitKey(0)
```

---

## 🛠️ Troubleshooting

* **Black/blank window**: Ensure the image path is correct and readable.
* **Colors look wrong**: Your `get_color` may need HSV conversion; try converting with `cv2.cvtColor(image, cv2.COLOR_BGR2HSV)` inside that function.
* **Missed shapes**: Adjust the threshold value (`70`) or add morphological operations before contouring.
* **Window not updating**: Remember to press a key for each detection because of `cv2.waitKey(0)` inside the loop.

---

## 🧭 Notes

* Works best on images with solid, contrasting shapes.
* If your shapes are hollow or have textures, consider edge detection (Canny) or adaptive thresholding.

---

## 📜 License

Free to use, modify, and learn from. Educational purposes welcome.
