<h1 align="center">🎥 OpenCV Python Tutorial Series</h1>

<p align="center">
  A complete, beginner-to-advanced, section-by-section guide to OpenCV with Python — with explained, copy-paste-ready code.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Complete-brightgreen" alt="Status">
</p>

---

## 📖 About

This repo is a complete collection of OpenCV Python tutorials, broken into focused sections. Each section covers one topic with **working code** and **line-by-line explanations** — no fluff, just what you need to actually understand what's happening under the hood.

Follow the sections in order for a structured path from zero to building real computer vision applications: images → manipulation → video → drawing → color/thresholding → filtering → edges/contours → detection.

---

## 📚 Table of Contents

| # | Section | Status |
|---|---------|--------|
| 1 | [Introduction & Images](#1-introduction--images) | ✅ Done |
| 2 | [Image Fundamentals and Manipulation](#2-image-fundamentals-and-manipulation) | ✅ Done |
| 3 | [Video Handling & Webcam Processing](#3-video-handling--webcam-processing) | ✅ Done |
| 4 | [Drawing Shapes & Text on Images](#4-drawing-shapes--text-on-images) | ✅ Done |
| 5 | [Color Spaces & Thresholding](#5-color-spaces--thresholding) | ✅ Done |
| 6 | [Blurring & Smoothing](#6-blurring--smoothing) | ✅ Done |
| 7 | [Edge Detection & Contours](#7-edge-detection--contours) | ✅ Done |
| 8 | [Face & Object Detection](#8-face--object-detection) | ✅ Done |

---

## ⚙️ Installation

```bash
pip install opencv-python numpy matplotlib
```

For extra/patented modules (SIFT, advanced feature detectors, etc.):
```bash
pip install opencv-contrib-python
```

> ⚠️ Don't install `opencv-python` and `opencv-contrib-python` together — they conflict since they share the same `cv2` namespace.

---

## 1. Introduction & Images

<details>
<summary><strong>Click to expand</strong></summary>

### What is OpenCV?
OpenCV (Open Source Computer Vision Library) is used for image processing, video analysis, and computer vision tasks. The Python bindings (`cv2`) give near-native speed with Python's simplicity.

### Reading an Image
```python
import cv2

img = cv2.imread('cat.jpg')
print(type(img))    # <class 'numpy.ndarray'>
print(img.shape)    # (height, width, channels)
```
Every image is loaded as a **NumPy array**. `cv2.imread()` silently returns `None` if the path is wrong — always check:
```python
if img is None:
    raise FileNotFoundError("Could not load image — check the path")
```

Read flags:
```python
cv2.imread('cat.jpg', cv2.IMREAD_COLOR)      # default, BGR
cv2.imread('cat.jpg', cv2.IMREAD_GRAYSCALE)  # single channel
cv2.imread('cat.jpg', cv2.IMREAD_UNCHANGED)  # keeps alpha channel
```

### Displaying an Image
```python
cv2.imshow('Cat', img)
cv2.waitKey(0)          # 0 = wait forever for a keypress
cv2.destroyAllWindows()
```
`cv2.waitKey(0)` is required — without it the window flashes and closes instantly.

### Saving an Image
```python
cv2.imwrite('cat_copy.png', img)
```

### BGR vs RGB ⚠️
OpenCV stores color images as **Blue-Green-Red**, not RGB. This trips people up constantly. Convert before using matplotlib/PIL:
```python
import matplotlib.pyplot as plt
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.show()
```

### Full Minimal Example
```python
import cv2

img = cv2.imread('cat.jpg')
if img is None:
    raise FileNotFoundError("Image not found")

print("Shape:", img.shape)
cv2.imshow('Original', img)
cv2.waitKey(0)
cv2.imwrite('cat_saved.jpg', img)
cv2.destroyAllWindows()
```

</details>

---

## 2. Image Fundamentals and Manipulation

<details>
<summary><strong>Click to expand</strong></summary>

### Images as NumPy Arrays
```python
import cv2
import numpy as np

img = cv2.imread('cat.jpg')
print(img.shape)  # (height, width, channels)
print(img.dtype)  # uint8 -> values 0-255
```
`dtype` is `uint8`, so arithmetic can **overflow/wrap around** unless handled carefully (see below).

### Accessing & Modifying Pixels
```python
pixel = img[100, 150]          # BGR order
img[100, 150] = [255, 255, 255]

region = img[50:150, 100:300]
img[0:100, 0:200] = [0, 255, 0]  # paint green rectangle
```
Indexing is `[row, col]` = `[y, x]` — **not** `[x, y]`. This is a common source of bugs.

### Cropping
```python
cropped = img[50:300, 100:400]  # just NumPy slicing, no special function needed
```

### Resizing
```python
resized = cv2.resize(img, (300, 200))          # (width, height)!
resized_scale = cv2.resize(img, None, fx=0.5, fy=0.5)
```
Interpolation options:
```python
cv2.resize(img, (300, 200), interpolation=cv2.INTER_AREA)   # best for shrinking
cv2.resize(img, (300, 200), interpolation=cv2.INTER_LINEAR) # default, general purpose
cv2.resize(img, (300, 200), interpolation=cv2.INTER_CUBIC)  # slower, better for enlarging
```

### Rotating
```python
(h, w) = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 45, 1.0)   # (center, angle, scale)
rotated = cv2.warpAffine(img, M, (w, h))
```
Quick 90°/180° rotation (no cropping issues):
```python
cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
cv2.rotate(img, cv2.ROTATE_180)
cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
```

### Flipping
```python
cv2.flip(img, 1)   # horizontal mirror
cv2.flip(img, 0)   # vertical flip
cv2.flip(img, -1)  # both
```

### Translating (Shifting)
```python
M = np.float32([[1, 0, 100], [0, 1, 50]])  # shift right 100px, down 50px
translated = cv2.warpAffine(img, M, (w, h))
```

### Arithmetic on Images
```python
bright = cv2.add(img, np.ones(img.shape, dtype='uint8') * 50)  # clips at 255

img2 = cv2.imread('dog.jpg')
img2 = cv2.resize(img2, (img.shape[1], img.shape[0]))  # must match size
blended = cv2.addWeighted(img, 0.7, img2, 0.3, 0)      # 70% img + 30% img2
```
`cv2.add()` performs **saturated** addition, clamping at 255. Plain NumPy `+` **wraps around** modulo 256 — usually not what you want.

### Splitting & Merging Channels
```python
b, g, r = cv2.split(img)
merged = cv2.merge([b, g, r])

zeros = np.zeros(img.shape[:2], dtype='uint8')
no_red = cv2.merge([b, g, zeros])
```

### Full Combined Example
```python
import cv2
import numpy as np

img = cv2.imread('cat.jpg')
if img is None:
    raise FileNotFoundError("Image not found")

cropped = img[50:300, 100:400]
resized = cv2.resize(cropped, (300, 200))

h, w = resized.shape[:2]
M = cv2.getRotationMatrix2D((w // 2, h // 2), 30, 1.0)
rotated = cv2.warpAffine(resized, M, (w, h))

bright = cv2.add(rotated, np.ones(rotated.shape, dtype='uint8') * 40)

cv2.imshow('Result', bright)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

</details>

---

## 3. Video Handling & Webcam Processing

<details>
<summary><strong>Click to expand</strong></summary>

### Reading from Webcam / Video File
```python
import cv2

cap = cv2.VideoCapture(0)  # 0 = default webcam, or pass a filename

if not cap.isOpened():
    raise IOError("Cannot open webcam/video source")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Video Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```
- `cap.read()` returns `(ret, frame)` — always check `ret` before using `frame`.
- `cv2.waitKey(1)` waits 1ms per frame (needed to render) and returns the key code; `& 0xFF` makes the comparison cross-platform safe.
- Always `cap.release()` when done, or the webcam device stays locked by your process.

### Getting/Setting Capture Properties
```python
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps    = cap.get(cv2.CAP_PROP_FPS)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

### Saving Video to Disk
```python
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)
    cv2.imshow('Recording', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
```
- `fourcc` is a 4-character codec code (`'XVID'` for `.avi`, `'mp4v'` for `.mp4`).
- `frame_size` passed to `VideoWriter` **must match** the actual frame dimensions, or the output file will be corrupted or empty.

</details>

---

## 4. Drawing Shapes & Text on Images

<details>
<summary><strong>Click to expand</strong></summary>

```python
import numpy as np
import cv2

canvas = np.zeros((500, 500, 3), dtype='uint8')  # blank black canvas

# Line: (image, pt1, pt2, color, thickness)
cv2.line(canvas, (0, 0), (500, 500), (0, 255, 0), 3)

# Rectangle: (image, top_left, bottom_right, color, thickness)
cv2.rectangle(canvas, (50, 50), (200, 200), (255, 0, 0), 2)
cv2.rectangle(canvas, (250, 250), (400, 400), (0, 0, 255), -1)  # -1 = filled

# Circle: (image, center, radius, color, thickness)
cv2.circle(canvas, (300, 100), 50, (0, 255, 255), 3)

# Ellipse: (image, center, axes, angle, startAngle, endAngle, color, thickness)
cv2.ellipse(canvas, (150, 350), (100, 50), 30, 0, 360, (255, 255, 0), 2)

# Text: (image, text, org, font, fontScale, color, thickness)
cv2.putText(canvas, 'OpenCV', (100, 470), cv2.FONT_HERSHEY_SIMPLEX,
            1.5, (255, 255, 255), 2)

cv2.imshow('Drawing', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

**Key points:**
- Coordinates for drawing functions are always `(x, y)` — the **opposite** of NumPy's `[row, col]` indexing used for pixel access. Easy to mix up.
- Thickness of `-1` fills the shape solid instead of drawing just the outline.
- `cv2.putText` needs a font constant (`cv2.FONT_HERSHEY_SIMPLEX` is the most common), a scale factor, and `org` = the bottom-left corner of the text.
- Draw on a **copy** of your image (`img.copy()`) to keep the original untouched — drawing functions modify arrays in place.

</details>

---

## 5. Color Spaces & Thresholding

<details>
<summary><strong>Click to expand</strong></summary>

### Color Space Conversion
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lab  = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
```
**HSV** (Hue, Saturation, Value) separates color from brightness, making it far better for color-based detection than BGR/RGB — lighting changes mostly affect V, not H.

### Color Masking with HSV
```python
import numpy as np

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_blue = np.array([100, 150, 50])
upper_blue = np.array([140, 255, 255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)   # 255 where blue, 0 elsewhere
result = cv2.bitwise_and(img, img, mask=mask)      # keep only blue regions
```

### Simple Thresholding
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
```
Threshold types:
```python
cv2.THRESH_BINARY      # pixel > thresh -> maxval, else 0
cv2.THRESH_BINARY_INV  # inverse of above
cv2.THRESH_TRUNC       # pixel > thresh -> thresh, else unchanged
cv2.THRESH_TOZERO      # pixel > thresh -> unchanged, else 0
```

### Adaptive Thresholding
Better for images with uneven lighting — computes a threshold per local region instead of one global value:
```python
adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)
```

### Otsu's Thresholding
Automatically picks the best global threshold value:
```python
ret, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

</details>

---

## 6. Blurring & Smoothing

<details>
<summary><strong>Click to expand</strong></summary>

```python
avg_blur   = cv2.blur(img, (5, 5))                  # simple averaging
gaussian   = cv2.GaussianBlur(img, (5, 5), 0)        # weighted blur
median     = cv2.medianBlur(img, 5)                  # great for salt-and-pepper noise
bilateral  = cv2.bilateralFilter(img, 9, 75, 75)     # smooths but preserves edges
```

**When to use which:**

| Function | Best for | Speed |
|---|---|---|
| `cv2.blur()` | Quick, low-quality smoothing | Fastest |
| `cv2.GaussianBlur()` | General-purpose, natural-looking blur | Fast |
| `cv2.medianBlur()` | Removing speckle/salt-and-pepper noise | Medium |
| `cv2.bilateralFilter()` | Smoothing while keeping edges sharp | Slowest |

Kernel sizes like `(5, 5)` must be **odd numbers**.

</details>

---

## 7. Edge Detection & Contours

<details>
<summary><strong>Click to expand</strong></summary>

### Edge Detection
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # reduce noise before edge detection
edges = cv2.Canny(blurred, 50, 150)          # (image, lower_thresh, upper_thresh)
```
`cv2.Canny()` finds edges via gradient intensity: pixels above the upper threshold are definite edges, below the lower are discarded, and those in between are kept only if connected to a strong edge. Blurring first reduces false edges from noise.

### Finding & Drawing Contours
```python
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

img_copy = img.copy()
cv2.drawContours(img_copy, contours, -1, (0, 255, 0), 2)  # -1 = draw all
```
- `cv2.RETR_EXTERNAL` retrieves only outermost contours; `cv2.RETR_TREE` retrieves the full nested hierarchy.
- `cv2.CHAIN_APPROX_SIMPLE` compresses redundant points to save memory vs. `cv2.CHAIN_APPROX_NONE`.

### Contour Properties
```python
for c in contours:
    area = cv2.contourArea(c)
    perimeter = cv2.arcLength(c, True)
    x, y, w, h = cv2.boundingRect(c)
    approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)  # simplify shape

    cv2.rectangle(img_copy, (x, y), (x + w, y + h), (255, 0, 0), 2)
```
`cv2.approxPolyDP()` approximates a contour with fewer vertices — useful for shape classification (e.g., a 4-vertex approx suggests a rectangle/square).

</details>

---

## 8. Face & Object Detection

<details>
<summary><strong>Click to expand</strong></summary>

```python
import cv2

# Load a pre-trained Haar Cascade classifier (ships with OpenCV)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

img = cv2.imread('people.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('Faces', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

**Parameters explained:**
- `cv2.data.haarcascades` points to the folder of pre-trained XML classifiers bundled with OpenCV (faces, eyes, smiles, full body, etc.).
- `scaleFactor` — how much the image is scaled down at each detection pass (1.1 = 10% reduction); smaller = more accurate but slower.
- `minNeighbors` — how many overlapping detections are required to confirm a real match; higher = fewer false positives, but risks missing real faces.

**Next step beyond Haar cascades:** OpenCV's **DNN module** (`cv2.dnn.readNet(...)`) supports modern deep-learning detectors (YOLO, SSD, Caffe/TensorFlow models) for much higher accuracy on general object detection.

</details>

---

## 🗂️ Repo Structure (Suggested)

```
opencv-python-tutorial/
├── README.md
├── requirements.txt
├── assets/
│   └── sample_images/
├── section_01_intro/
├── section_02_fundamentals/
├── section_03_video/
├── section_04_drawing/
├── section_05_color_thresholding/
├── section_06_blurring/
├── section_07_edges_contours/
└── section_08_detection/
```

---

## 🧭 Learning Path Summary

```
Images (read/show/save)
        ↓
Manipulation (crop, resize, rotate, blend)
        ↓
Video (webcam, recording)
        ↓
Drawing (shapes, text, annotations)
        ↓
Color Spaces & Thresholding (HSV, masks, binary images)
        ↓
Blurring & Smoothing (noise reduction)
        ↓
Edge Detection & Contours (shape analysis)
        ↓
Face & Object Detection (Haar cascades → DNN)
```

---

## 🤝 Contributing

Found an issue or want to suggest a topic for a future section (e.g., DNN-based detection, feature matching, camera calibration)? Open an issue or PR — contributions welcome.

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">Made with ☕ and lots of <code>cv2.imshow()</code> debugging</p>
