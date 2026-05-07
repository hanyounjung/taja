import streamlit as st
import time
import random
import pandas as pd
from streamlit_ace import st_ace

st.set_page_config(page_title="Python 코드 타자연습", page_icon="⌨️")

st.title("⌨️ Python 코드 타자연습")
st.write("제시된 Python 코드를 똑같이 입력해 보세요.")

problems = [
    'print("Hello, Python!")',
    'name = input("이름을 입력하세요: ")',
    'age = int(input("나이를 입력하세요: "))',
    'score = 90\nif score >= 60:\n    print("합격입니다")',
    'for i in range(5):\n    print(i)',
    'fruits = ["apple", "banana", "cherry"]\nfor fruit in fruits:\n    print(fruit)',
    'def hello():\n    print("안녕하세요")',
    'student = {"name": "Kim", "age": 17}\nprint(student["name"])'
]

if "problem" not in st.session_state:
    st.session_state.problem = random.choice(problems)

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "records" not in st.session_state:
    st.session_state.records = []

if "editor_key" not in st.session_state:
    st.session_state.editor_key = 0

name = st.text_input("👤 이름을 입력하세요")

st.subheader("제시 코드")
st.code(st.session_state.problem, language="python")

user_input = st_ace(
    value="",
    language="python",
    theme="github",
    key=f"editor_{st.session_state.editor_key}",
    height=220,
    auto_update=True,
    tab_size=4,
    font_size=16,
    wrap=True
)

col1, col2 = st.columns(2)

with col1:
    if st.button("결과 확인"):
        if name.strip() == "":
            st.warning("이름을 입력하세요.")
        else:
            target = st.session_state.problem
            elapsed = time.time() - st.session_state.start_time

            correct = sum(1 for a, b in zip(target, user_input) if a == b)
            accuracy = correct / len(target) * 100

            words = len(user_input.split())
            wpm = words / (elapsed / 60) if elapsed > 0 else 0

            if accuracy >= 90:
                message = "훌륭해요 🎉"
            elif accuracy >= 70:
                message = "좋아요 😊"
            else:
                message = "다시 도전 💪"

            st.success(message)
            st.write(f"⏱ 시간: {elapsed:.1f}초")
            st.write(f"🎯 정확도: {accuracy:.1f}%")
            st.write(f"⚡ 속도: {wpm:.1f} WPM")

            st.session_state.records.append({
                "이름": name,
                "정확도(%)": round(accuracy, 1),
                "속도(WPM)": round(wpm, 1),
                "시간(초)": round(elapsed, 1),
                "결과": message
            })

with col2:
    if st.button("새 문제"):
        st.session_state.problem = random.choice(problems)
        st.session_state.start_time = time.time()
        st.session_state.editor_key += 1
        st.rerun()

if st.session_state.records:
    st.subheader("📊 기록")
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)
