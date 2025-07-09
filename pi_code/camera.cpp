// camera.cpp -- Raspberry Pi Camera Streaming via libcamera-vid

#include "camera.h"
#include <cstdlib>    // For std::system
#include <iostream>   // For std::cout, std::cerr
#include <string>     // For std::string

/**
 * Starts an MJPEG camera stream using libcamera-vid on the specified TCP port.
 */
void start_camera_stream(int port) {
    // Build command to launch libcamera-vid as a background process streaming MJPEG
    std::string command =
        "libcamera-vid "
        "--camera 0 "                    // Use camera port
        "-t 0 "                          // Stream indefinitely
        "--width 640 --height 480 "     // Set resolution
        "--codec mjpeg "                // Use MJPEG format
        "--listen "                     // Enable TCP streaming
        "-o tcp://0.0.0.0:" + std::to_string(port) +
        " > /dev/null 2>&1 &";          // Suppress output and run in background

    std::cout << "CAMERA Starting MJPEG stream on port " << port << "\n";

    // Execute the system command
    int result = std::system(command.c_str());
    if (result != 0) {
        std::cerr << "CAMERA Failed to launch stream, return code: " << result << "\n";
    }
}

/**
 * Captures a still image and saves it to the specified file.
 */
void take_still_photo(const char* filename) {
    // Construct command to take a still image with libcamera-still
    std::string command =
        "libcamera-still --camera 0 -o " + std::string(filename) + " > /dev/null 2>&1";

    std::cout << "CAMERA Taking photo: " << filename << "\n";
    std::system(command.c_str());
}

/**
 * Records a short video clip to the specified file.
 */
void start_camera_video(const char* filename, int duration_ms) {
    // Build command to record a video using libcamera-vid
    std::string command =
        "libcamera-vid --camera 0 "
        "-t " + std::to_string(duration_ms) +
        " --width 640 --height 480 -o " + filename + " > /dev/null 2>&1 &";

    std::cout << "CAMERA Recording video to: " << filename << "\n";
    std::system(command.c_str());
}