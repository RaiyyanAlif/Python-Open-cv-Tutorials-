<h1 align="center">🎥 OpenCV Python Tutorial Series</h1>

<p align="center">
  A beginner-to-advanced, section-by-section guide to OpenCV with Python — with explained, copy-paste-ready code.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-In%20Progress-yellow" alt="Status">
</p>

---

## 📖 About

This repo is a growing collection of OpenCV Python tutorials, broken into digestible sections. Each section covers a focused topic with **working code** and **line-by-line explanations** — no fluff, just what you need to actually understand what's happening.

Whether you're just starting out with computer vision or brushing up on fundamentals, follow the sections in order for a structured path from zero to building real CV applications.

---

## 📚 Table of Contents

| # | Section | Status |
|---|---------|--------|
| 1 | [Introduction & Images](#1-introduction--images) | ✅ Done |
| 2 | [Image Fundamentals and Manipulation](#2-image-fundamentals-and-manipulation) | ✅ Done |
| 3 | Video Handling & Webcam Processing | 🔜 Coming Soon |
| 4 | Drawing Shapes & Text on Images | 🔜 Coming Soon |
| 5 | Color Spaces & Thresholding | 🔜 Coming Soon |
| 6 | Blurring & Smoothing | 🔜 Coming Soon |
| 7 | Edge Detection & Contours | 🔜 Coming Soon |
| 8 | Face & Object Detection | 🔜 Coming Soon |

> More sections added as the series progresses. ⭐ Star the repo to keep track of updates.

---

## ⚙️ Installation

```bash
pip install opencv-python numpy matplotlib
```

For extra/patented modules (SIFT, etc.):
```bash
pip install opencv-contrib-python
```

> ⚠️ Don't install `opencv-python` and `opencv-contrib-python` together — they conflict.

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

### Saving an Image
```python
cv2.imwrite('cat_copy.png', img)
```

### BGR vs RGB ⚠️
OpenCV stores color images as **Blue-Green-Red**, not RGB. Convert before using matplotlib/PIL:
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
`dtype` is `uint8`, so arithmetic can **overflow/wrap around** unless handled carefully.

### Accessing & Modifying Pixels
```python
pixel = img[100, 150]          # BGR order
img[100, 150] = [255, 255, 255]

region = img[50:150, 100:300]
img[0:100, 0:200] = [0, 255, 0]  # paint green rectangle
```
Indexing is `[row, col]` = `[y, x]` — **not** `[x, y]`.

### Cropping
```python
cropped = img[50:300, 100:400]  # just NumPy slicing
```

### Resizing
```python
resized = cv2.resize(img, (300, 200))          # (width, height)!
resized_scale = cv2.resize(img, None, fx=0.5, fy=0.5)
```
Interpolation options:
```python
cv2.resize(img, (300, 200), interpolation=cv2.INTER_AREA)   # shrinking
cv2.resize(img, (300, 200), interpolation=cv2.INTER_LINEAR) # default
cv2.resize(img, (300, 200), interpolation=cv2.INTER_CUBIC)  # enlarging
```

### Rotating
```python
(h, w) = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(img, M, (w, h))
```
Quick 90°/180° rotation:
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
M = np.float32([[1, 0, 100], [0, 1, 50]])  # shift right 100, down 50
translated = cv2.warpAffine(img, M, (w, h))
```

### Arithmetic on Images
```python
bright = cv2.add(img, np.ones(img.shape, dtype='uint8') * 50)  # clips at 255

img2 = cv2.imread('dog.jpg')
img2 = cv2.resize(img2, (img.shape[1], img.shape[0]))
blended = cv2.addWeighted(img, 0.7, img2, 0.3, 0)
```
`cv2.add()` **clips** at 255; plain NumPy `+` **wraps around** — usually not what you want.

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

## 🗂️ Repo Structure (Suggested)

```
opencv-python-tutorial/
├── README.md
├── requirements.txt
├── assets/
│   └── sample_images/
├── section_01_intro/
│   └── intro.py
├── section_02_fundamentals/
│   └── manipulation.py
└── section_03_video/
    └── (coming soon)
```

---

## 🤝 Contributing

Found an issue or want to suggest a topic for the next section? Open an issue or PR — contributions welcome.

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">Made with ☕ and lots of <code>cv2.imshow()</code> debugging</p>
