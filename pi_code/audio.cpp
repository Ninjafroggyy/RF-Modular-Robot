// audio.cpp — USB Microphone Audio Streaming Server
//
// This module sets up a TCP server on the Raspberry Pi to stream live audio
// from a USB microphone to a connected client (e.g., a remote control app).
// It uses arecord to capture audio and streams raw PCM data over the socket.

#include "audio.h"

#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include <iostream>

#define BACKLOG 1
#define BUFFER_SIZE 1024

/**
 * Launches a TCP server on the given port. When a client connects, the Pi
 * captures microphone input using arecord and sends the audio stream as
 * raw PCM data over the socket.
 */
void start_audio_stream(int port) {
    int server_fd, client_fd;
    struct sockaddr_in addr{};
    socklen_t addr_len = sizeof(addr);

    // Create socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("Audio: Socket failed");
        return;
    }

    // Allow address reuse to avoid bind issues after restart
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    // Configure server address
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;       // Accept connections on any interface
    addr.sin_port = htons(port);             // Convert port to network byte order

    // Bind socket to the port
    if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("Audio: Bind failed");
        close(server_fd);
        return;
    }

    // Start listening for one client
    listen(server_fd, BACKLOG);
    std::cout << "Audio: Listening on port " << port << "...\n";

    // Accept incoming client connection
    client_fd = accept(server_fd, (struct sockaddr *)&addr, &addr_len);
    std::cout << "Audio: Client connected. Streaming...\n";

    // Start arecord to capture audio input from USB mic
    FILE* mic = popen("arecord -D plughw:2,0 -f cd", "r");
    if (!mic) {
        std::cerr << "Audio: Failed to open arecord stream.\n";
        close(client_fd);
        close(server_fd);
        return;
    }

    // Read and stream audio data in chunks
    char buffer[BUFFER_SIZE];
    while (!feof(mic)) {
        size_t bytes = fread(buffer, 1, sizeof(buffer), mic);
        if (bytes > 0) {
            send(client_fd, buffer, bytes, 0);
        }
    }

    // Clean up resources
    pclose(mic);
    close(client_fd);
    close(server_fd);
    std::cout << "Audio: Stream closed.\n";
}
