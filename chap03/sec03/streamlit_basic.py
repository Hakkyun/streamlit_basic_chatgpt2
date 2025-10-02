import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError, APIStatusError

# 1) 로컬 .env (Cloud에서는 없어도 됨)
load_dotenv()

# 2) 키 읽기: Secrets(우선) → ENV
API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("API Key가 비어있습니다. Streamlit Secrets 또는 .env를 확인하세요.")
    st.stop()

client = OpenAI(api_key=API_KEY)

st.title("37조 변학균 최지은 챕터8 점심은 뭐먹지 바로 고궁")

# 대화 상태 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "원하는거 말해봐 인간아?"}]

# 기록 렌더링
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 입력 처리
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # 먼저 접근 쉬운 모델로 테스트
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        reply = resp.choices[0].message.content

    except AuthenticationError as e:
        st.error(f"[Auth] 인증 오류: {e}")
        st.stop()
    except RateLimitError as e:
        st.error(f"[429] 호출 제한: {e}")
        st.stop()
    except APIConnectionError as e:
        st.error(f"[네트워크] 연결 실패: {e}")
        st.stop()
    except APIStatusError as e:
        st.error(f"[{e.status_code}] API 오류: {e.message}")
        st.stop()
    except Exception as e:
        st.error(f"[기타] {type(e).__name__}: {e}")
        st.stop()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
