# conversation.py
import base64
from helper import (
    encode_audio_to_base64,
    record_audio,
    save_audio_file,
    summarize_conversation,
    audio_to_chinese_transcript,
)
from teacher import send_message


def conversation_loop(client):
    lesson_prompt = """
    你是一名资深汉语教师，你只会说普通话，不会说韩语。你教学时要使用自然的中文语速和表达，只有在示范需要学生跟读的句子时才放慢速度。因为你的学生是韩国人，汉语水平是初级。
    你必须在称呼学生时使用他们的名字，并加上同学。你必须在上课之前问候学生。
    请按照以下课程计划持续进行对话，不要设定固定的对话轮数，而是根据学生的反应和学习进度自然地继续教学。每轮对话包括：
    1. 首先，用温暖友好的语气向学生问好，并示范朗读一句中文，在示范句子时要放慢速度，例如：「我喜欢吃苹果」，邀请学生跟读。
    2. 在学生跟读后，请认真聆听学生的发音。如果学生发音完全正确，请给予充分鼓励，表现出真诚的喜悦和兴奋，使用更加生动活泼的语调和表达方式；如果有错误，请用耐心的语气指出具体的错误（如某个字或音节发音不准），并提供正确发音的示范与改进建议。
    3. 随后，提出下一句练习句子，句子可逐渐增加难度，如：「今天我们一起读书」或「你喜欢吃水果吗？」等。
    4. 每次回答后，必须以提问或指令结束，例如使用指令'一起读'或'请再说一遍'，以确保课堂互动性。
    5. 重要：无论学生用什么语言回复，你都只能使用中文回应。即使学生用韩语或其他语言提问，你也只能用中文回答，必要时可以使用更简单的中文词汇或短句来帮助学生理解，但绝对不要使用韩语。
    6. 当学生表现优秀时，你应该表现出真实的喜悦和热情，用更加生动、活泼的语调表达赞扬，就像真正的老师会做的那样。使用丰富的肢体语言描述（如拍手、竖起大拇指等）来增强你的表达效果。
    7. 持续进行教学，不要主动结束对话，始终保持教学的连续性和互动性。
    """

    conversation_summary = """
    \n[CONVERSATION SUMMARY]\n"""

    # lesson 세팅
    conversation_history = [
        {"role": "user", "content": [{"type": "text", "text": lesson_prompt}]}
    ]
    counter = 1
    teacher_transcript, audio_id = send_message(conversation_history, counter, client)
    # conversation_history.append({"role": "assistant", "content": teacher_transcript})
    # conversation_history.append({"role": "assistant", "audio": {"id": audio_id}})

    conversation_summary = summarize_conversation(
        conversation_summary=conversation_summary,
        role="teacher",
        transcript=teacher_transcript,
        counter=counter,
        client=client,
    )

    conversation_history = [
        {
            "role": "user",
            "content": [{"type": "text", "text": lesson_prompt + conversation_summary}],
        }
    ]

    while True:
        counter += 1

        input("엔터키를 눌러 녹음을 시작하세요...")
        student_audio_bytes = record_audio(duration=5, fs=16000)
        student_filename = f"{counter}_student.wav"
        save_audio_file(student_audio_bytes, student_filename)
        student_encoded = encode_audio_to_base64(student_audio_bytes)

        # student_text = input("텍스트 답변을 입력하세요 (없으면 엔터): ")
        # if not student_text.strip():
        #     student_text = "학생의 음성 답변만 첨부되었습니다."

        student_message = {
            "role": "user",
            "content": [
                # {
                #     "type": "text",
                #     "text": student_text
                # },
                {
                    "type": "input_audio",
                    "input_audio": {"data": student_encoded, "format": "wav"},
                },
            ],
        }
        conversation_history.append(student_message)
        student_transcript = audio_to_chinese_transcript(student_audio_bytes, client)

        conversation_summary = summarize_conversation(
            conversation_summary=conversation_summary,
            role="student",
            transcript=student_transcript,
            counter=counter,
            client=client,
        )

        counter += 1
        teacher_transcript, audio_id = send_message(
            conversation_history, counter, client
        )
        # conversation_history.append({"role": "assistant", "audio": {"id": audio_id}})
        conversation_summary = summarize_conversation(
            conversation_summary=conversation_summary,
            role="teacher",
            transcript=teacher_transcript,
            counter=counter,
            client=client,
        )

        conversation_history = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": lesson_prompt + conversation_summary}
                ],
            }
        ]

        print()
        print("conversation_summary: ", conversation_summary)
        print()

        user_continue = input("대화를 계속하려면 엔터, 종료하려면 'q'를 입력하세요: ")
        if user_continue.lower() == "q":
            print("수업 대화를 종료합니다.")
            break
