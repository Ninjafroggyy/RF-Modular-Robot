// utils.c — Shared Utility Function Definitions


#include <stdio.h>
#include "utils.h"


void log_message(const char* level, const char* module, const char* message) {
   printf("[%s][%s] %s\n", level, module, message);
}




