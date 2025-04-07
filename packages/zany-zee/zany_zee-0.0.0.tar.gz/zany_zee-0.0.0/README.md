# 🎨 Zany Zee

Zany Zee is a Python library that combines powerful features for **photo, video, audio, and animation manipulation** into one seamless experience. Whether you're building content creation tools or enhancing multimedia with AI, Zany Zee is your all-in-one solution.

## ✨ Features

### 🔤 Content Loader
- Load and display text, images, and videos
- Apply basic visual transformations
- Add watermarks and shapes

### 🤖 Mediant (AI Tools)
- Enhance images and videos
- Remove backgrounds
- Detect objects and faces
- Stabilize videos
- Generate thumbnails and AI avatars

### 🔊 Anidio Processor (Audio)
- Control volume and speed
- Remove noise
- Convert formats
- Merge, split, or reverse audio

### 🎞️ Animation
- Manage frames
- Play, pause, loop, reverse animations
- Create animated GIFs
- Add flashing text effects

### 🎛 Filters
- Apply grayscale, sepia, blur, sharpen
- Cartoonize images
- Detect edges
- Adjust contrast and brightness

## 📦 Installation
pip install zanyzee


## 🧪 Example Usage

from zanyzee.mediant import Mediant

media = Mediant()
media.enhance_image("input.jpg", "enhanced.jpg")


## 🛠 Requirements
Python 3.7+
opencv-python
numpy
Pillow
moviepy
pydub
rembg


## Install them via:
pip install -r requirements.txt


## 📂 Project Structure
zanyzee/
├── __init__.py
├── content_loader.py
├── mediant.py
├── anidio_processor.py
├── animation.py
├── filters.py


## 🧑‍💻 Author

Made with ❤️ by Kishan Kachhadiya