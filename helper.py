import base64
import io
import wave
import sounddevice as sd
import numpy as np


def encode_audio_to_base64(audio_bytes):
    return base64.b64encode(audio_bytes).decode("utf-8")


def save_audio_file(audio_bytes, filename):
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    print(f"오디오 파일이 저장되었습니다: {filename}")


def record_audio(duration=5, fs=16000):
    """
    마이크로부터 지정된 시간 동안 음성을 녹음하고,
    메모리 내 WAV 파일(byte stream)로 반환합니다.
    """
    print("녹음 시작...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()  # 녹음 완료까지 대기
    print("녹음 완료.")

    with io.BytesIO() as wav_io:
        with wave.open(wav_io, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # int16의 경우 2바이트
            wf.setframerate(fs)
            wf.writeframes(audio_data.tobytes())
        wav_bytes = wav_io.getvalue()
    return wav_bytes
