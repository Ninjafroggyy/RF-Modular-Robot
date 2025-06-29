// command.c — Movement Command Server
//
// This module starts a TCP server that listens for remote movement commands
// such as "forward", "back", "left", "right", and "stop". These are received
// as plain text strings and translated into movement control functions
// (implemented in movement.h / movement.c).

#include "movement.h"
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BUF_SIZE 1024

/**
 * Starts a TCP server on the given port to receive movement commands.
 * On client connection, it listens for string-based commands and
 * triggers the corresponding robot movement functions.
 */
void start_command_server(int port) {
    int server_fd, client_fd;
    struct sockaddr_in addr;
    char buffer[BUF_SIZE];

    // Create TCP socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);

    // Set up server address (listen on all interfaces)
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(port);

    // Bind socket to the port
    bind(server_fd, (struct sockaddr*)&addr, sizeof(addr));

    // Start listening for a single client
    listen(server_fd, 1);
    printf("Control server listening on port %d\n", port);

    // Accept client connection
    socklen_t len = sizeof(addr);
    client_fd = accept(server_fd, (struct sockaddr*)&addr, &len);
    printf("Control client connected\n");

    // Listen for incoming text-based commands
    while (1) {
        memset(buffer, 0, BUF_SIZE);                       // Clear buffer
        int r = recv(client_fd, buffer, BUF_SIZE - 1, 0);  // Receive data
        if (r <= 0) break;                                 // Exit loop if disconnected

        printf("Control %s\n", buffer);                     // Debug print

        // Match and trigger movement commands
        if (strstr(buffer, "forward"))       move_forward();
        else if (strstr(buffer, "back"))     move_backward();
        else if (strstr(buffer, "left"))     move_left();
        else if (strstr(buffer, "right"))    move_right();
        else if (strstr(buffer, "stop"))     stop_movement();
    }

    // Clean up
    close(client_fd);
    close(server_fd);
}
