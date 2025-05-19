# Eta-Bemax (Engineering Project) – Medical Assistance Robot

## 🚩 Table of Contents

- [Introduction](#-introduction)
- [Module Installation](#-module-installation)
- [Guidelines](#-guidelines)
- [Features](#-features)
- [Usage](#-usage)
- [Authors](#-authors)

## 🤖 Introduction
The goal of this project is to develop a semi-autonomous robot capable of assisting individuals in medical need, particularly those unable to move or reach supplies themselves. Eta-Bemax is designed for lab settings with flat, unobstructed flooring, where it can provide emergency aid without requiring human assistance.

The robot addresses three common lab-related injuries:
- Burns
- Cuts
- Eye infections

Each injury type corresponds to a dedicated compartment in the robot, stocked with the appropriate medical supplies. When a person is in need, they can say the wake word "help me." Upon detecting the wake word, the robot will activate its camera and object detection model to locate a human in the room. Once the human is centered in the frame, Eta-Bemax autonomously approaches the user. When it reaches a predefined proximity threshold, it stops and triggers all servo-controlled compartments to open.

In parallel, a Flask-based web app provides manual control of the robot’s movement and compartments. It also includes:
- A directional control pad for movement
- Real-time status updates and error logs
- Toggle buttons to open/close compartments

## 📦 Module Installation
To run Eta-Bemax, install the following dependencies:
```pip install flask```<br>
```pip install flask-sqlalchemy```<br>
```pip install flask-login```<br>
```pip install gpiozero```<br>
```pip install pvporcupine```<br>
```pip install speechrecognition```<br>
```pip install opencv-python```<br>
```pip install adafruit-circuitpython-pca9685```<br>

## 🔧 Guidelines
| Language   | Tools |
|------------|-------|
| Python     |[Flask](https://flask.palletsprojects.com/en/2.1.x/ ), [GPIOZero](https://gpiozero.readthedocs.io/en/latest/), [PicoVoice](https://picovoice.ai/platform/porcupine/), [OpenCV](https://docs.opencv.org/4.x/d0/de3/tutorial_py_intro.html)     |
| JavaScript |DOM manipulation, button handling       |
| HTML/CSS   |Custom templates, Figma for prototyping       |

## 🎨 Features
- Custom Wake-Word Activation: Trained on “help me” using PicoVoice.
- Voice Commands: Supports “Come here” and “Open compartments” with live speech-to-text.
- Visual Human Detection: Rotates until a person is in view, then approaches and stops at a set distance.
- Servo-Controlled Compartments: All open/close simultaneously to deliver supplies.
- Web Admin Interface: Manual control, error logs, and dynamic toggle between open/closed states.
- Automatic Timeout Logic: Stops rotation or compartment operation if no command is detected.

## 🐾 Usage
1. Navigate to the project directory and run the Flask server: ```python3 app.py```
2. Open your browser and go to http://localhost:5000

## 🌏 Authors
Chloe Chow
Ivy Lee
Piyawan Chaiprasit
