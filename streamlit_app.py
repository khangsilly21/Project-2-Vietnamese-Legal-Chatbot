import streamlit as st
from resourses import get_chat_engine, get_query_engine, get_index, get_llm, get_embed_model

st.set_page_config(page_title="MARky - Vietnamese Legal Chabot", page_icon="🤖", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Vietnamese Legal Chabot")

# st.info(" ", icon="📃")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Chào bạn, **MARky** là trợ lý AI hỗ trợ phân tích, trả lời câu hỏi về pháp luật hôn nhân gia đình Việt Nam, với sứ mệnh mang luật pháp tới gần hơn với mọi người mọi người.",
        }
    ]

index = get_index()

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = get_chat_engine()

if prompt := st.chat_input(
    "Ask a question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Write message history to UI
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response_stream = st.session_state.chat_engine.stream_chat(prompt)
        st.write_stream(response_stream.response_gen)
        message = {"role": "assistant", "content": response_stream.response}
        # Add response to message history
        st.session_state.messages.append(message)
        

