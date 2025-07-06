// movement.c — Motor Control Using libgpiod

#include "movement.h"
#include <gpiod.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define the GPIO chip name (default for Raspberry Pi)
#define CHIP_NAME "gpiochip0"

// Define GPIO line numbers for motor control (adjust if using different pins)
#define GPIO_IN1 17
#define GPIO_IN2 18
#define GPIO_IN3 27
#define GPIO_IN4 22

// Static handles to the GPIO chip and lines
static struct gpiod_chip* chip;
static struct gpiod_line* in1;
static struct gpiod_line* in2;
static struct gpiod_line* in3;
static struct gpiod_line* in4;

// Initialise GPIO lines for motor control
void init_motors() {
    chip = gpiod_chip_open_by_name(CHIP_NAME);
    if (!chip) {
        perror("MOTOR Failed to open GPIO chip");
        exit(1);
    }

    // Get each motor control GPIO line
    in1 = gpiod_chip_get_line(chip, GPIO_IN1);
    in2 = gpiod_chip_get_line(chip, GPIO_IN2);
    in3 = gpiod_chip_get_line(chip, GPIO_IN3);
    in4 = gpiod_chip_get_line(chip, GPIO_IN4);

    if (!in1 || !in2 || !in3 || !in4) {
        perror("MOTOR Failed to get one or more GPIO lines");
        exit(1);
    }

    // Request output mode for each line
    gpiod_line_request_output(in1, "motor", 0);
    gpiod_line_request_output(in2, "motor", 0);
    gpiod_line_request_output(in3, "motor", 0);
    gpiod_line_request_output(in4, "motor", 0);

    // Ensure motors are stopped initially
    stop_movement();
    printf("MOTOR Initialised GPIO lines.\n");
}

// Release all motor GPIO lines and cleanup
void cleanup_motors() {
    stop_movement();

    gpiod_line_release(in1);
    gpiod_line_release(in2);
    gpiod_line_release(in3);
    gpiod_line_release(in4);
    gpiod_chip_close(chip);

    printf("MOTOR GPIO cleanup complete.\n");
}

// Helper function to set all 4 motor control lines
void set_lines(int a, int b, int c, int d) {
    gpiod_line_set_value(in1, a);
    gpiod_line_set_value(in2, b);
    gpiod_line_set_value(in3, c);
    gpiod_line_set_value(in4, d);
}

// Move robot forward
void move_forward() {
    set_lines(1, 0, 1, 0);
    printf("MOTOR Moving forward\n");
}

// Move robot backward
void move_backward() {
    set_lines(0, 1, 0, 1);
    printf("MOTOR Moving backward\n");
}

// Turn robot left
void move_left() {
    set_lines(0, 1, 1, 0);
    printf("MOTOR Turning left\n");
}

// Turn robot right
void move_right() {
    set_lines(1, 0, 0, 1);
    printf("MOTOR Turning right\n");
}

// Stop all motor movement
void stop_movement() {
    set_lines(0, 0, 0, 0);
    printf("MOTOR Stopped\n");
}