import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI

def main():
    st.set_page_config(page_title='🧠MemoryBot🤖', layout='wide')

    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []
    if "input" not in st.session_state:
        st.session_state["input"] = ""
    if "stored_session" not in st.session_state:
        st.session_state["stored_session"] = []

    st.title("🤖 Chat Bot with 🧠")
    st.subheader(" Powered by 🦜 LangChain + OpenAI + Streamlit")

    api_key = st.sidebar.text_input("API-KEY", type="password")

    if api_key:
        initialize_conversation(api_key)
        run_chat()

def initialize_conversation(api_key):
    llm = OpenAI(temperature=0, openai_api_key=api_key, verbose=False)

    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=10)

    st.session_state.Conversation = ConversationChain(
        llm=llm,
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=st.session_state.entity_memory
    )

def run_chat():
    st.sidebar.button("New Chat", on_click=new_chat, type='primary')
    user_input = get_text()

    if user_input:
        output = st.session_state.Conversation.run(input=user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    display_conversation_history()

def get_text():
    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                               placeholder="Your AI assistant here! Ask me anything ...",
                               label_visibility='hidden')
    return input_text

def new_chat():
    save_chat_session()
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.entity_store = {}
    st.session_state.entity_memory.buffer.clear()

def save_chat_session():
    save = []
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])
    st.session_state["stored_session"].append(save)

def display_conversation_history():
    download_str = []
    with st.expander("Conversation", expanded=True):
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            st.info(st.session_state["past"][i], icon="🧐")
            st.success(st.session_state["generated"][i], icon="🤖")
            download_str.append(st.session_state["past"][i])
            download_str.append(st.session_state["generated"][i])

        download_str = '\n'.join(download_str)
        if download_str:
            st.download_button('Download', download_str)

    for i, sublist in enumerate(st.session_state.stored_session):
        with st.sidebar.expander(label=f"Conversation-Session:{i}"):
            st.write(sublist)

    if st.session_state.stored_session:
        if st.sidebar.checkbox("Clear-all"):
            del st.session_state.stored_session

if __name__ == "__main__":
    main()
