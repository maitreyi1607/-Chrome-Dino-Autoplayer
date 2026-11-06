# 🦖 Chrome Dino Autoplayer

An automated Chrome Dino game player built using **Python, OpenCV, NumPy, PyAutoGUI, and Arduino Uno**.

The system detects obstacles in real time using computer vision and automatically controls a servo motor to physically press the spacebar, allowing the Dino to jump over approaching obstacles.

## 🚀 Project Overview

The Chrome Dino Autoplayer uses computer vision to identify cacti and flying birds in the Chrome Dino game.

Python processes the game screen using OpenCV, calculates the distance to approaching obstacles, and sends jump commands to an Arduino Uno through serial communication.

The Arduino controls an SG90 servo motor, which physically presses the laptop's spacebar.

## ✨ Features

- Real-time object detection using OpenCV.
- Cactus detection in light and dark themes.
- Bird detection.
- Dino and obstacle distinction.
- Nearest obstacle distance calculation.
- Automatic jump triggering.
- Prevention of unnecessary jumps.
- Python-to-Arduino serial communication.
- Physical spacebar pressing using an SG90 servo motor.
- Continuous automated gameplay.

## 🛠️ Technologies Used

### Software
- Python
- OpenCV
- NumPy
- PyAutoGUI
- PySerial
- Arduino IDE
- VS Code

### Hardware
- Arduino Uno R3
- SG90 Servo Motor
- USB Cable
- Jumper Wires

## ⚙️ Working Methodology

1. Python captures the Chrome Dino game screen.
2. OpenCV processes the captured image.
3. The game area is cropped and converted into grayscale.
4. Thresholding and contour detection identify obstacles.
5. Detected objects are filtered and classified.
6. The distance to the nearest obstacle is calculated.
7. A jump condition is triggered when an obstacle approaches.
8. Python sends a command to Arduino through serial communication.
9. Arduino receives the command and controls the servo motor.
10. The servo physically presses the spacebar, making the Dino jump.

## 📦 Python Libraries

Install the required libraries:

```bash
pip install opencv-python numpy pyautogui pyserial
```

## ▶️ How to Run

1. Connect the Arduino Uno to your computer.
2. Upload the Arduino servo control code using Arduino IDE.
3. Open the Chrome Dino game.
4. Update the serial port in the Python code according to your Arduino connection.
5. Run the Python program.

```bash
python main.py
```

## 🎯 Project Objective

The objective of this project is to combine computer vision, Python programming, and embedded hardware to develop an automated game-playing system.

It demonstrates real-time image processing, object detection, serial communication, and hardware control.

## 👩‍💻 Project Status

**Completed** ✅

Developed as a hands-on project exploring the integration of software and hardware systems.
