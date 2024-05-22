import streamlit as st
import os

import time
import jwt
import requests


# 实际KEY，过期时间
def generate_token(apikey: str, exp_seconds: int):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)

    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }
    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )


def ask_glm(key, model, max_tokens, temperature, content):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': generate_token(key, 1000)
    }

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": content
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


st.set_page_config(page_title="聊天机器人")

with st.sidebar:
    st.title('通过API与大模型的对话')
    # st.write('支持的大模型包括的ChatGLM3和4')
    if 'API_TOKEN' in st.session_state and len(st.session_state['API_TOKEN']) > 1:
        st.success('API Token已经配置', icon='✅')
        key = st.session_state['API_TOKEN']
    else:
        key = ""

    key = st.text_input('输入Token:', type='password', value=key)

    st.session_state['API_TOKEN'] = key

    model = st.selectbox("选择模型", ["glm-3-turbo", "glm-4"])
    max_tokens = st.slider("max_tokens", 0, 2000, value=512)
    temperature = st.slider("temperature", 0.0, 2.0, value=0.8)

# 初始化的对话
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "你好我是ChatGLM，有什么可以帮助你的？"}]

# 将保留的历史对话展示在界面上。（由于这是一个演示性的代码，随着时间的增加，对话记录会越来越多，导致token的消耗会变大）
# 建议只保留最近10条对话，需要在调用模型时st.session_state.messages做一些处理，限制发往LLM的对话记录的条数
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "你好我是ChatGLM，有什么可以帮助你的？"}]


st.sidebar.button('清空聊天记录', on_click=clear_chat_history)

# 当用户输入了key之后，才可以显示对话信息。
if len(key) > 1:
    # 界面上绘制输入框，并且将用户输入的内容添加到对话列表中
    if prompt := st.chat_input():
        # 将用户输入的文字（提示词）添加到message中。
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("请求中..."):
                full_response = \
                ask_glm(key, model, max_tokens, temperature, st.session_state.messages)['choices'][0]['message'][
                    'content']
                st.markdown(full_response)
                # 将LLM响应的内容也作为对话历史的一部分
                message = {"role": "assistant", "content": full_response}
                st.session_state.messages.append(message)
