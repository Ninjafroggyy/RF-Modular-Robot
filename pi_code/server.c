/* multi_port_server.c
   Simulates a Raspberry Pi server with:
   - Control server (JSON over TCP, port 5000)
   - Audio stream server (dummy PCM sine wave, port 5001)
   - Camera stream server (test JPEG loop, port 5002)
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <math.h>
#include <fcntl.h>
#include <sys/stat.h>

#define CTRL_PORT   5000
#define AUDIO_PORT  5001
#define CAM_PORT    5002
#define BUF_SIZE    1024

void *command_server_thread(void *arg);
void *audio_stream_thread(void *arg);
void *camera_stream_thread(void *arg);

int main() {
    pthread_t t1, t2, t3;

    pthread_create(&t1, NULL, command_server_thread, NULL);
    pthread_create(&t2, NULL, audio_stream_thread, NULL);
    pthread_create(&t3, NULL, camera_stream_thread, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);

    return 0;
}

// ────────────────────────────────────────────────────────────────
void *command_server_thread(void *arg) {
    int server_fd, client_fd;
    struct sockaddr_in addr;
    char buffer[BUF_SIZE];

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(CTRL_PORT);

    bind(server_fd, (struct sockaddr*)&addr, sizeof(addr));
    listen(server_fd, 1);
    printf("[✓] Control server listening on port %d\n", CTRL_PORT);

    socklen_t len = sizeof(addr);
    client_fd = accept(server_fd, (struct sockaddr*)&addr, &len);
    printf("[→] Control client connected\n");

    while (1) {
        memset(buffer, 0, BUF_SIZE);
        int r = recv(client_fd, buffer, BUF_SIZE - 1, 0);
        if (r <= 0) break;
        printf("[CTRL] %s\n", buffer);
    }
    close(client_fd);
    close(server_fd);
    return NULL;
}

// ────────────────────────────────────────────────────────────────
void *audio_stream_thread(void *arg) {
    int server_fd, client_fd;
    struct sockaddr_in addr;
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(AUDIO_PORT);

    bind(server_fd, (struct sockaddr*)&addr, sizeof(addr));
    listen(server_fd, 1);
    printf("[✓] Audio server listening on port %d\n", AUDIO_PORT);

    socklen_t len = sizeof(addr);
    client_fd = accept(server_fd, (struct sockaddr*)&addr, &len);
    printf("[→] Audio client connected\n");

    // Send sine wave PCM data
    const int SAMPLE_RATE = 44100;
    const double freq = 440.0;
    short sample;
    for (int i = 0; i < SAMPLE_RATE * 10; i++) { // 10 sec
        sample = (short)(32767 * sin(2 * M_PI * freq * i / SAMPLE_RATE));
        send(client_fd, &sample, sizeof(sample), 0);
    }

    close(client_fd);
    close(server_fd);
    return NULL;
}

// ────────────────────────────────────────────────────────────────
void *camera_stream_thread(void *arg) {
    int server_fd, client_fd;
    struct sockaddr_in addr;
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(CAM_PORT);

    bind(server_fd, (struct sockaddr*)&addr, sizeof(addr));
    listen(server_fd, 1);
    printf("[✓] Camera server listening on port %d\n", CAM_PORT);

    socklen_t len = sizeof(addr);
    client_fd = accept(server_fd, (struct sockaddr*)&addr, &len);
    printf("[→] Camera client connected\n");

    // Load a test JPEG
    const char *jpeg_path = "test.jpg";
    FILE *fp = fopen(jpeg_path, "rb");
    if (!fp) {
        perror("Failed to open test.jpg");
        close(client_fd);
        close(server_fd);
        return NULL;
    }
    fseek(fp, 0, SEEK_END);
    long fsize = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    char *jpeg_data = malloc(fsize);
    fread(jpeg_data, 1, fsize, fp);
    fclose(fp);

    // Stream JPEG repeatedly
    for (int i = 0; i < 1000; i++) {
        send(client_fd, jpeg_data, fsize, 0);
        usleep(100000); // 10 fps
    }

    free(jpeg_data);
    close(client_fd);
    close(server_fd);
    return NULL;
}