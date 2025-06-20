import sounddevice as sd
import scipy.io.wavfile


def start_audio_stream():
    print("[MOCK] Playing test audio clip")
    fs, data = scipy.io.wavfile.read("test_assets/fake_audio.wav")
    sd.play(data, samplerate=fs)
