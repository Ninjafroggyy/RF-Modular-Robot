// server.c — Unified Pi Server for Camera, Audio, and Movement
//
// Launches all backend modules for the robot system using separate threads:
// - Camera stream server
// - USB microphone audio stream server
// - Movement command server
//
// Each server runs independently and listens on its designated TCP port.

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "camera.h"
#include "audio.h"
#include "movement.h"

// ── Port Configuration ───────────────────────────────────────────────
#define CAMERA_PORT 5002  // Port used by MJPEG camera stream
#define AUDIO_PORT  5001  // Port used by USB microphone audio stream
#define CTRL_PORT   5000  // Port used for control commands (movement)

// ── Thread Wrappers for Each Module ──────────────────────────────────

/**
 * Thread function to start the camera stream server.
 */
void* camera_thread(void* _) {
    start_camera_stream(CAMERA_PORT);
    return NULL;
}

/**
 * Thread function to start the audio stream server.
 */
void* audio_thread(void* _) {
    start_audio_stream(AUDIO_PORT);
    return NULL;
}

/**
 * Thread function to start the control command server.
 */
void* command_thread(void* _) {
    start_command_server(CTRL_PORT);
    return NULL;
}

// ── Main Startup Function ─────────────────────────────────────────────

/**
 * Launches camera, audio, and movement servers on separate threads.
 * Each server listens on its own port and runs independently.
 * The function blocks until all threads exit.
 */
void start_robot_system() {
    pthread_t cam_tid, audio_tid, ctrl_tid;

    printf("Server: Launching camera, audio, and control modules...\n");

    // Start all server threads
    pthread_create(&cam_tid, NULL, camera_thread, NULL);
    pthread_create(&audio_tid, NULL, audio_thread, NULL);
    pthread_create(&ctrl_tid, NULL, command_thread, NULL);

    // Wait for all threads to finish
    pthread_join(cam_tid, NULL);
    pthread_join(audio_tid, NULL);
    pthread_join(ctrl_tid, NULL);

    printf("Server: All modules terminated.\n");
}
