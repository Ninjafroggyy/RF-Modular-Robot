// main.c — Entry Point for Modular Robot System
// This is the main executable file that starts the robot system.
// It initialises and launches the backend modules defined in main.h (e.g. camera, audio, control).
#include <stdio.h>
#include "main.h"

/**
 * Entry point for the robot program.
 * Calls the `start_robot_system()` function, which launches all communication and module servers.
 */
int main() {
   printf("Starting modular robot system...\n");
   start_robot_system();
   printf("Robot system terminated.\n");
   return 0;
}


