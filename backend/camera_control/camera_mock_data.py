import cv2


def get_current_frame():
    """
    Return a test image frame from disk as fake camera input.
    """
    frame = cv2.imread("test_assets/fake_frame.jpg")
    return frame
