import base64
import io
import wave
import sounddevice as sd


def encode_audio_to_base64(audio_bytes):
    return base64.b64encode(audio_bytes).decode("utf-8")


def save_audio_file(audio_bytes, filename):
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    print(f"오디오 파일이 저장되었습니다: {filename}")


def save_pcm_file(pcm_data, filename, channels=1, sample_width=2, frame_rate=22000):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)  # 모노: 1, 스테레오: 2 등
        wf.setsampwidth(sample_width)  # 일반적으로 2바이트 (16비트)
        wf.setframerate(frame_rate)  # 예: 44100Hz
        wf.writeframes(pcm_data)
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


def translate_chinese_to_korean(chinese_text, client):
    translation_prompt = f"다음 중국어 텍스트를 한국어로 번역해줘:\n\n{chinese_text}"

    completion = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": translation_prompt}]
    )

    translated_text = completion.choices[0].message.content
    return translated_text


def audio_to_chinese_transcript(audio_bytes, client):
    # 학생의 발음을 정확하게 텍스트로 변환
    transcript_prompt = """
    学生: [沉默]  
    老师: 你可以再试一次吗？  

    学生: [发音不清]  
    老师: 请慢慢来，我们一起读：「我喜欢吃苹果」。  

    学生: 我喜欢吃苹果  
    老师: 很好！你的发音很标准！  
    """

    audio_io = io.BytesIO(audio_bytes)
    audio_io.name = "student_audio.wav"

    transcript = client.audio.transcriptions.create(
        model="gpt-4o-transcribe", file=audio_io, prompt=transcript_prompt
    )

    return transcript.text


def summarize_conversation(conversation_summary, role, transcript, counter, client):
    conversation_summary += f"{counter}. {role}: {transcript}\n"

    # 추후 요약 모델 붙이기
    return conversation_summary
