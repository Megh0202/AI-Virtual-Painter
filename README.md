**AI Virtual Painter**

An AI-powered virtual painting application that lets you draw, erase, and switch colors in real-time using just your hand gestures and a webcam. Built with OpenCV and MediaPipe for hand tracking.
🚀 Features

🎨 Draw with your index finger — no mouse or stylus needed.

✌️ Selection mode with two fingers — choose colors, brush, or eraser.

🖼️ Interactive toolbar (Header images) for tool & color selection.

🧠 Real-time hand tracking powered by Mediapipe.

🧽 Eraser mode with adjustable thickness.

📷 Canvas overlay to blend drawing with live video.

│── Ai_virtualPainter.py      # Main painter script (Part 1)
│── HandTrackingModule.py  # Hand tracking class (Part 2)

Install dependencies:

pip install opencv-python mediapipe numpy

▶Usage

Place toolbar images in the Header/ folder. (e.g., brush, eraser, colors)

Run the script:

python VirtualPainter.py


Use your webcam to:

✌️ Raise two fingers (index + middle) to select tools/colors.

☝️ Raise only index finger to start drawing.

🖤 Select black to activate the eraser.


Tech Stack

Python 3.x
OpenCV – image processing & video capture
MediaPipe – real-time hand tracking
NumPy – image array manipulation

**Future Improvements**
Add more brush styles & colors
Save drawings as image files
Multi-hand drawing support
Gesture-based undo/redo



