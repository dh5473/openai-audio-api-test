# teacher.py
import base64
import time
from helper import save_audio_file, translate_chinese_to_korean


def send_message(conversation_history, counter, client):
    messages = conversation_history.copy()

    start_time = time.time()

    completion = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
        messages=messages,
    )
    end_time = time.time()
    print()
    print("model_latency: ", end_time - start_time)

    message = completion.choices[0].message
    transcript = message.audio.transcript if message.audio else ""
    audio_id = message.audio.id if message.audio else None

    print("===== AI 응답 =====")
    print(transcript)

    # 한국어로 번역
    if transcript:
        translation = translate_chinese_to_korean(transcript, client)
        print("=== AI 한국어 번역 메시지 ===")
        print(translation)
    else:
        print("녹취된 텍스트가 없어 번역을 수행할 수 없습니다.")

    # 오디오 저장
    try:
        if message.audio:
            audio_b64 = message.audio.data
            audio_bytes = base64.b64decode(audio_b64)
            save_audio_file(audio_bytes, f"{counter}_teacher.wav")
    except Exception as e:
        print("AI 음성 저장 중 에러 발생:", e)
    print()

    return transcript, audio_id
