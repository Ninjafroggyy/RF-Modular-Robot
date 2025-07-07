#ifndef MOVEMENT_H
#define MOVEMENT_H

#ifdef __cplusplus
extern "C" {
#endif

void init_motors();
void cleanup_motors();
void move_forward();
void move_backward();
void move_left();
void move_right();
void stop_movement();

#ifdef __cplusplus
}
#endif

#endif
