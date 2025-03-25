from helper import record_audio, save_audio_file

input("엔터키를 눌러 녹음을 시작하세요...")
# duration으로 녹음 시간(초)을 조절할 수 있습니다!
audio_bytes = record_audio(duration=5, fs=16000)
student_filename = f"new_record.wav"
save_audio_file(audio_bytes, student_filename)
