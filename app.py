import streamlit as st
import time
import random
import pandas as pd

st.title("⌨️ Python 코드 타자연습")

# 👉 학생 이름 입력
name = st.text_input("👤 이름을 입력하세요")

# 👉 문장 리스트
sentences = [
    'print("Hello, Python!")',
    'name = input("이름을 입력하세요: ")',
    'age = int(input("나이를 입력하세요: "))',
    'score = 90',
    'if score >= 60:\n    print("합격입니다")',
    'for i in range(5):\n    print(i)',
    'fruits = ["apple", "banana", "cherry"]',
    'for fruit in fruits:\n    print(fruit)',
    'def hello():\n    print("안녕하세요")',
    'student = {"name": "Kim", "age": 17}',
    'print(student["name"])'
]

# 👉 세션 초기화
if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(sentences)
    st.session_state.start_time = time.time()

if "records" not in st.session_state:
    st.session_state.records = []

# 👉 문제 표시
st.subheader("제시 코드")
st.code(st.session_state.sentence)

# 👉 입력창 (key 중요!)
user_input = st.text_area("코드를 그대로 입력하세요", key="input_area")

# 👉 결과 확인
if st.button("결과 확인"):
    if name == "":
        st.warning("이름을 입력하세요!")
    else:
        end_time = time.time()
        elapsed = end_time - st.session_state.start_time

        correct = sum(1 for a, b in zip(st.session_state.sentence, user_input) if a == b)
        accuracy = correct / len(st.session_state.sentence) * 100

        words = len(user_input.split())
        wpm = words / (elapsed / 60)

        st.success("결과")
        st.write(f"⏱ 시간: {elapsed:.1f}초")
        st.write(f"🎯 정확도: {accuracy:.1f}%")
        st.write(f"⚡ 속도: {wpm:.1f} WPM")

        # 👉 기록 저장
        st.session_state.records.append({
            "이름": name,
            "정확도": round(accuracy, 1),
            "속도(WPM)": round(wpm, 1),
            "시간(초)": round(elapsed, 1)
        })

# 👉 새 문제 버튼 (입력창 초기화 핵심!)
if st.button("새 문제"):
    st.session_state.sentence = random.choice(sentences)
    st.session_state.start_time = time.time()

    # 🔥 입력창 초기화
    st.session_state.input_area = ""

    st.rerun()

# 👉 기록 표시
if st.session_state.records:
    st.subheader("📊 기록")
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df)
