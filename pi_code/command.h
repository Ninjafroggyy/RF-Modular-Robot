// command.h — Command Server Interface
#ifndef COMMAND_H
#define COMMAND_H

#ifdef __cplusplus
extern "C" {
#endif

// Start the TCP server for receiving movement commands
void start_command_server(int port);

#ifdef __cplusplus
}
#endif

#endif
