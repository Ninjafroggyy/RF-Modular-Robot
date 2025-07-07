// camera.h — Cross-compatible C/C++ interface for Pi camera control
#ifndef CAMERA_H
#define CAMERA_H

#ifdef __cplusplus
extern "C" {
#endif

void start_camera_stream(int port);
void take_still_photo(const char* filename);
void start_camera_video(const char* filename, int duration_ms);

#ifdef __cplusplus
}
#endif

#endif
