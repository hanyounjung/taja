import streamlit as st
from streamlit_ace import st_ace
import time
import random
import pandas as pd

st.title("⌨️ Python 코드 타자연습")

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

if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(sentences)

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "records" not in st.session_state:
    st.session_state.records = []

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

name = st.text_input("👤 이름을 입력하세요")

st.subheader("제시 코드")
st.code(st.session_state.sentence)

user_input = st_ace(
    value="",
    language="python",
    theme="monokai",
    key=f"ace_{st.session_state.input_key}",
    height=200,
    auto_update=True
)

if st.button("결과 확인"):
    if name.strip() == "":
        st.warning("이름을 입력하세요!")
    else:
        elapsed = time.time() - st.session_state.start_time

        target = st.session_state.sentence
        correct = sum(1 for a, b in zip(target, user_input) if a == b)
        accuracy = correct / len(target) * 100

        words = len(user_input.split())
        wpm = words / (elapsed / 60) if elapsed > 0 else 0

        st.success("결과")
        st.write(f"⏱ 시간: {elapsed:.1f}초")
        st.write(f"🎯 정확도: {accuracy:.1f}%")
        st.write(f"⚡ 속도: {wpm:.1f} WPM")

        st.session_state.records.append({
            "이름": name,
            "제시 코드": target,
            "정확도": round(accuracy, 1),
            "속도(WPM)": round(wpm, 1),
            "시간(초)": round(elapsed, 1)
        })

if st.button("새 문제"):
    st.session_state.sentence = random.choice(sentences)
    st.session_state.start_time = time.time()

    # 입력창 초기화 핵심
    st.session_state.input_key += 1

    st.rerun()

if st.session_state.records:
    st.subheader("📊 기록")
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df)
