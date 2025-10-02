import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 2) Cloud/로컬 겸용으로 키 읽기 (Secrets > ENV 순)
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("API Key가 설정되지 않았습니다. Streamlit Secrets 또는 .env를 확인하세요.")
    st.stop()

client = OpenAI(api_key=api_key)

st.title("37조 변학균 최지은 챕터8 점심은 뭐먹지 바로 고궁")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "원하는거 말해봐 인간아?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 최신 SDK 문법 그대로 사용
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
