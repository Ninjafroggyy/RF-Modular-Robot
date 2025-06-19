# Modular RF-Controlled Robot System

**University Group Project** | Sprint-Led Development | Raspberry Pi 5

---

## Overview

This project explores the development of a **modular, wirelessly controlled robot platform** using a Raspberry Pi 5. It demonstrates modularity in both **hardware and software**, with interchangeable components and terrain adaptability.

The robot is controlled from a **custom Python GUI app** running on a laptop, sending commands over 2.4GHz to the Pi, which interfaces with a camera, microphone, and robot chassis.

Designed and built by a team of three, this sprint-led build is intended as both a functional prototype and a shared learning experience.

---

## Project Goals

- Modular robot chassis using RC car base or chassis kit
- Wireless control via custom Python GUI
- Real-time video/audio stream from robot to laptop
- Interchangeable hardware modules (camera, mic, wheels)
- Clear backend/frontend structure for collaborative coding
- Unit tests and mock data for test-driven development

---

## Repository Structure

```bash
RF_Modular_Robot/
│
├── backend/ # Logic for robot control, network, audio/video
│ ├── movement.py
│ ├── network.py
│ ├── camera.py
│ └── audio.py
│
├── frontend/ # Pygame-based GUI interface
│ └── app.py
│
├── tests/ # Unit tests using Python's unittest module
│ ├── test_movement.py
│ ├── test_network.py
│ ├── test_camera.py
│ └── test_audio.py
│
├── main.py # Entry point – launches GUI
└── requirements.txt

```

---

## Mock & Testing Support

This project supports development **without hardware** by using:

- Mocked backend behavior (e.g., simulated movement commands)
- Fake video frames via local images
- Test `.wav` audio clips for audio playback simulation
- Unit testing with `unittest`

To run all unit tests:

```bash
python -m unittest discover -s tests

```

## Skills Focus

- **Modular Python architecture**
- **Embedded system integration** (Raspberry Pi + peripherals)
- **Event-driven GUI development** using `pygame`
- **Network socket communication**
- **Test-driven development** (mocking, assertions)
- **Real-time system interaction and debugging**

## 📅 Sprint Scope

This is a **5-day sprint project**, with a hard deadline.

> The aim is a working prototype that demonstrates **modularity and communication**.  
> If a task isn’t completed in time, we move forward — progress over perfection

