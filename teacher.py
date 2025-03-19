# teacher.py
import base64
import time
from helper import save_audio_file


def translate_chinese_to_korean(chinese_text, client):
    translation_prompt = f"다음 중국어 텍스트를 한국어로 번역해줘:\n\n{chinese_text}"

    completion = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": translation_prompt}]
    )

    translated_text = completion.choices[0].message.content
    return translated_text


def send_teacher_message(prompt_text, client):
    """
    AI 선생님의 초기 메시지를 생성하고, 오디오 응답을 저장합니다.
    """
    start_time = time.time()

    completion = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt_text}]}],
    )
    message = completion.choices[0].message

    end_time = time.time()
    print("model_latency: ", end_time - start_time)

    # AI 선생님이 생성한 오디오 정보 가져오기
    audio_id = message.audio.id if message.audio else None
    transcript = message.audio.transcript if message.audio else ""

    print("=== AI 선생님 초기 메시지 ===")
    print(transcript)

    # 한국어 번역본 생성
    if transcript:
        translation = translate_chinese_to_korean(transcript, client)
        print("=== AI 선생님 한국어 번역 메시지 ===")
        print(translation)
    else:
        print("녹취된 텍스트가 없어 번역을 수행할 수 없습니다.")

    # 오디오 파일 저장
    try:
        if message.audio:
            audio_b64 = message.audio.data
            audio_bytes = base64.b64decode(audio_b64)
            save_audio_file(audio_bytes, "teacher_initial_response.wav")
    except Exception as e:
        print("AI 선생님 음성 저장 중 에러 발생:", e)

    return message, audio_id


def send_teacher_response(conversation_history, client, counter):
    """
    대화 기록을 기반으로 AI 선생님이 후속 응답을 생성합니다.
    - 이전 오디오의 audio.id를 활용하여 일관된 오디오 대화를 유지합니다.
    """
    messages = conversation_history.copy()

    start_time = time.time()
    
    completion = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
        messages=messages,
    )
    message = completion.choices[0].message

    end_time = time.time()
    print("model_latency: ", end_time - start_time)

    audio_id = message.audio.id if message.audio else None
    transcript = message.audio.transcript if message.audio else ""

    print("=== AI 선생님 응답 ===")
    print(transcript)

    # 한국어 번역본 생성
    if transcript:
        translation = translate_chinese_to_korean(transcript, client)
        print("=== AI 선생님 한국어 번역 메시지 ===")
        print(translation)
    else:
        print("녹취된 텍스트가 없어 번역을 수행할 수 없습니다.")

    try:
        if message.audio:
            audio_b64 = message.audio.data
            audio_bytes = base64.b64decode(audio_b64)
            save_audio_file(audio_bytes, f"{counter}_teacher.wav")
    except Exception as e:
        print("AI 선생님 음성 저장 중 에러 발생:", e)

    return transcript, audio_id
