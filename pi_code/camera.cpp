#include "camera.h"
#include <cstdlib>
#include <string>
#include <iostream>

void start_camera_video(const char* filename, int duration_ms) {
    std::string command = "libcamera-vid -t " + std::to_string(duration_ms) +
                          " --width 640 --height 480 -o " + filename + " > /dev/null 2>&1 &";
    std::cout << "[Camera] Starting video recording: " << filename << "\n";
    system(command.c_str());
}

void take_still_photo(const char* filename) {
    std::string command = "libcamera-still -o " + std::string(filename) + " > /dev/null 2>&1";
    std::cout << "[Camera] Taking still photo: " << filename << "\n";
    system(command.c_str());
}


main.cpp

#include "camera.h"

int main() {
    take_still_photo("test.jpg");
    start_camera_video("test.h264", 3000);  // 3 seconds
    return 0;
}



// Compile with:  g++ camera_streamer.cpp -o camstream
// Run with:      ./camstream
//
// This launches libcamera-vid in MJPEG mode and streams
// indefinitely on TCP port 5001.

#include <cstdlib>
#include <iostream>
#include <string>

int main() {
    // 640×480 @ ~20 fps MJPEG streamed over TCP
    std::string cmd =
        "libcamera-vid "
        "-t 0 "                  // unlimited duration
        "--width 640 --height 480 "
        "--codec mjpeg "
        "--listen "
        "-o tcp://0.0.0.0:5001 "
        "> /dev/null 2>&1";

    std::cout << "[Camera] Streaming on tcp://<pi-ip>:5001\n";
    int ret = system(cmd.c_str());

    if (ret != 0)
        std::cerr << "[Camera] libcamera-vid returned " << ret << "\n";

    return ret;
}
