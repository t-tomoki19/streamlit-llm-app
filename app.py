from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.5,
    openai_api_key=os.environ["OPENAI_API_KEY"]
)


expert_prompts = {
    "健康アドバイザー": "あなたは健康に関するアドバイザーです。安全で信頼できるアドバイスを日本語で提供してください。",
    "キャリアカウンセラー": "あなたは経験豊富なキャリアカウンセラーです。日本語で的確かつ親身なキャリアアドバイスを行ってください。",
}

def ask_expert(expert_name: str, user_input: str) -> str:
    messages = [
        SystemMessage(content=expert_prompts[expert_name]),
        HumanMessage(content=user_input)
    ]
    response = llm(messages)
    return response.content

st.title("ch6課題アプリ：専門家AIに相談しよう")

st.write("##### モード1: 健康 or キャリアに関する相談")
st.write("AI専門家が回答します。")

st.divider()

expert_type = st.radio("相談したい専門家を選んでください：", list(expert_prompts.keys()), horizontal=True)

user_message = st.text_area("相談内容を入力してください：", height=150)

if st.button("実行"):
    if user_message.strip():
        with st.spinner("AIが考えています..."):
            try:
                result = ask_expert(expert_type, user_message)
                st.success("AI専門家からの回答")
                st.write(result)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("相談内容を入力してください。")