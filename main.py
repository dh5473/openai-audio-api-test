# main.py
from dotenv import load_dotenv
import os
from openai import OpenAI
from conversation import conversation_loop


def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY가 설정되어 있지 않습니다. .env 파일을 확인하세요.")
        return

    client = OpenAI(api_key=api_key)
    conversation_loop(client)


if __name__ == "__main__":
    main()
