import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, APIStatusError, APIConnectionError, AuthenticationError, RateLimitError

load_dotenv()
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API Key가 비어있습니다. Secrets 또는 .env 확인!")
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

    try:
        # 일단 접근성이 더 널널한 모델로 테스트
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        msg = resp.choices[0].message.content

    except AuthenticationError as e:
        st.error(f"[Auth] 인증 오류: {e}. 키/Secrets 확인 필요.")
        st.stop()
    except RateLimitError as e:
        st.error(f"[429] 레이트리밋: {e}. 요청 빈도/사용량 확인.")
        st.stop()
    except APIStatusError as e:
        # HTTP 상태코드/서버 응답 바디까지 표시
        st.error(f"[{e.status_code}] API 오류\nResponse: {e.response}\nMessage: {e.message}")
        st.stop()
    except APIConnectionError as e:
        st.error(f"[네트워크] API 연결 실패: {e}")
        st.stop()
    excep
