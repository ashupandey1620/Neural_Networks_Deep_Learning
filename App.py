import streamlit as st
import requests


# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)


# ============================================
# TITLE
# ============================================

st.title("🤖 RAG Chatbot")


# ============================================
# SESSION STATE
# ============================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================
# DISPLAY CHAT HISTORY
# ============================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================
# USER INPUT
# ============================================

query = st.chat_input(
    "Ask something about the document..."
)


# ============================================
# HANDLE CHAT
# ============================================

if query:

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })


    with st.chat_message("user"):

        st.markdown(query)


    with st.spinner("Thinking..."):

        try:

            response = requests.post(
                "http://localhost:8000/chat",
                json={
                    "question": query
                }
            )

            data = response.json()


            if "detail" in data:

                answer = data["detail"]

            else:

                answer = data["answer"]


            with st.chat_message("assistant"):

                st.markdown(answer)


                if "sources" in data:

                    with st.expander("Sources"):

                        for i, source in enumerate(data["sources"]):

                            st.markdown(f"### Source {i+1}")

                            st.write(source)


            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:

            st.error(str(e))
