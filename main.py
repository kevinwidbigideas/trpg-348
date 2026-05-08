import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from dotenv import load_dotenv
import os

load_dotenv()

def main():
    mock = os.getenv("MOCK_LLM", "true").lower() == "true"
    print("348차원 소설 세계관 체험 시스템")
    print(f"LLM 모드: {'MOCK' if mock else 'REAL'}")
    print(f"Qdrant: {os.getenv('QDRANT_HOST')}:{os.getenv('QDRANT_PORT')}")

if __name__ == "__main__":
    main()
