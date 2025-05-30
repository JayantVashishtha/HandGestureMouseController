# Hand Gesture-Based Mouse Controller

A real-time system that enables mouse control using hand gestures captured from a webcam. This project leverages computer vision and machine learning techniques to provide a touchless way of interacting with your computer using intuitive hand gestures.

---

## Features

- Move mouse cursor by tracking the index finger.
- Perform **left click**, **right click**, and **double click** using specific finger gestures.
- Capture screenshots with an **open palm** gesture.
- Real-time hand tracking with high accuracy using MediaPipe.
- Custom gesture recognition based on finger angles and distances.

---

## Tech Stack

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- Pynput
- NumPy

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Jayant Vashishtha/hand-gesture-mouse-controller.git
   cd hand-gesture-mouse-controller
   
2. python -m venv venv
   
3. source venv/bin/activate     # On Windows: venv\Scripts\activate

4. pip install -r requirements.txt
   
5. Run:
     python main.py
