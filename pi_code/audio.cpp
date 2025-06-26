#include <arpa/inet.h>
#include <unistd.h>
#include <cstdlib>
#include <cstring>
#include <iostream>

#define PORT 5000

int main() {
    int server_fd, client_fd;
    struct sockaddr_in address;
    socklen_t addrlen = sizeof(address);

    // ── Create socket ───────────────────────────────
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == 0) {
        perror("socket failed");
        return 1;
    }

    // ── Bind to port ────────────────────────────────
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY; // Listen on any interface
    address.sin_port = htons(PORT);
    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 1);

    std::cout << "[Mic] Waiting for client to connect on port " << PORT << "...\n";
    client_fd = accept(server_fd, (struct sockaddr *)&address, &addrlen);
    std::cout << "[Mic] Client connected. Streaming audio...\n";

    // ── Open arecord pipe ───────────────────────────
    FILE* mic = popen("arecord -D plughw:1,0 -f cd", "r");  // 16-bit, 44.1kHz, stereo

    char buffer[1024];
    while (!feof(mic)) {
        size_t bytes = fread(buffer, 1, sizeof(buffer), mic);
        if (bytes > 0) {
            send(client_fd, buffer, bytes, 0);
        }
    }

    pclose(mic);
    close(client_fd);
    close(server_fd);
    return 0;
}

