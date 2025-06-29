# ─── Compiler and Flags ─────────────────────────────────────────────
CC      = gcc
CXX     = g++
CFLAGS  = -Wall -Wextra -pthread
CXXFLAGS = -Wall -Wextra -pthread -std=c++17


OPENCV_CFLAGS = `pkg-config --cflags opencv4`
OPENCV_LIBS   = `pkg-config --libs opencv4`


INCLUDES = -I/usr/include/opencv4


# ─── Source Files ───────────────────────────────────────────────────
C_SRC   = main.c server.c utils.c movement.c command.c
CPP_SRC = audio.cpp camera.cpp


C_OBJ   = $(C_SRC:.c=.o)
CPP_OBJ = $(CPP_SRC:.cpp=.o)


TARGET = robot_server


# ─── Build Rules ────────────────────────────────────────────────────
all: $(TARGET)


$(TARGET): $(C_OBJ) $(CPP_OBJ)
   $(CXX) $(CXXFLAGS) $(C_OBJ) $(CPP_OBJ) -o $@ $(OPENCV_LIBS)


# Compile .c files with gcc
%.o: %.c
   $(CC) $(CFLAGS) -c $< -o $@


# Compile .cpp files with g++ and OpenCV
%.o: %.cpp
   $(CXX) $(CXXFLAGS) $(OPENCV_CFLAGS) -c $< -o $@


clean:
   rm -f *.o $(TARGET)


