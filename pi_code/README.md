# Modular Robot Server (C Code) — Raspberry Pi

This directory contains the C/C++ source code used to control the Raspberry Pi components in our university group project. It is responsible for handling:

- USB microphone audio streaming
- Camera image/video streaming (MJPEG)
- Movement control via socket commands
- Multithreaded server setup

## Structure

- `main.c` — Entry point that launches all modules via threads.
- `server.c` — Manages the threaded startup of audio, camera, and movement servers.
- `audio.cpp` — Streams raw audio data from a USB microphone to a connected client over TCP.
- `camera.cpp` — Streams MJPEG frames captured from the Pi camera to a client over TCP.
- `command.c` — Listens for control commands (e.g., "forward", "stop") and passes them to the motor module.
- `movement.c` — Handles GPIO logic to drive the motors.
- Header files (`.h`) — Provide function declarations and simple module descriptions.

## Build Instructions

Make sure `g++`, `opencv4`, and threading support are available.

Use the following command to compile:
```
make clean && make
```

## Runtime Info

The compiled binary launches three servers simultaneously:

- Port `5000`: Movement control
- Port `5001`: Audio streaming
- Port `5002`: Camera stream

These are expected to be consumed by the Python frontend via sockets.

## Notes

- Camera functionality requires a connected camera module and may need to be modified depending on camera hardware.
- Audio assumes the microphone appears as `plughw:2,0` — run `arecord -l` to verify device index.

