// camera.cpp — Raspberry Pi Camera Streaming via libcamera-vid
#include "camera.h"
#include <cstdlib>
#include <iostream>
#include <string>

void start_camera_stream(int port) {
    std::string command =
        "libcamera-vid "
        "--camera 1 "                    // Use second camera port
        "-t 0 "                          // Unlimited duration
        "--width 640 --height 480 "
        "--codec mjpeg "
        "--listen "
        "-o tcp://0.0.0.0:" + std::to_string(port) +
        " > /dev/null 2>&1 &";

    std::cout << "[Camera] Starting MJPEG stream on port " << port << "\n";

    int result = std::system(command.c_str());
    if (result != 0) {
        std::cerr << "[Camera] Failed to launch stream, return code: " << result << "\n";
    }
}

void take_still_photo(const char* filename) {
    std::string command =
        "libcamera-still --camera 1 -o " + std::string(filename) + " > /dev/null 2>&1";
    std::cout << "[Camera] Taking photo: " << filename << "\n";
    std::system(command.c_str());
}

void start_camera_video(const char* filename, int duration_ms) {
    std::string command =
        "libcamera-vid --camera 1 "
        "-t " + std::to_string(duration_ms) +
        " --width 640 --height 480 -o " + filename + " > /dev/null 2>&1 &";
    std::cout << "[Camera] Recording video to: " << filename << "\n";
    std::system(command.c_str());
}
