import socket
import pyaudio

def audio_stream_loop():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    HOST = '192.168.77.2'
    #HOST = '10.15.224.11'
    PORT = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

    try:
        while True:
            data = client_socket.recv(CHUNK)
            if not data:
                break
            stream.write(data)
    except Exception as e:
        print("[Audio Stream Error]:", e)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        client_socket.close()