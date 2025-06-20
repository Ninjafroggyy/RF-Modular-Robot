""" Handles receiving and decoding video stream from the Pi. """

import cv2
import numpy as np

stream_url = "http://192.168.1.42:8080/video"  # Example MJPEG stream
cap = None


def start_video_stream():
    """ Start the video stream from the Pi. """
    global cap
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("[ERROR] Failed to open video stream.")


def stop_video_stream():
    """Stop the video stream."""
    global cap
    if cap:
        cap.release()
        cap = None


def get_current_frame():
    """
    Return the latest video frame as an image (for rendering).
    Returns:
        frame (numpy.ndarray or None): Current video frame
    """
    if not cap:
        return None
    ret, frame = cap.read()
    if not ret:
        return None
    return frame
