import streamlit as st
from langchain.chains import ConversationChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma

# Check if persistence is enabled and a directory exists
PERSIST = True  # Set this to your preference
# if PERSIST and os.path.exists("persist"):
print("Reusing index...\n")
vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
index = VectorStoreIndexWrapper(vectorstore=vectorstore)
loader = DirectoryLoader("data/")
index = VectorstoreIndexCreator().from_loaders([loader])

# Set up the conversation chain with memory
llm = ChatOpenAI(
                 openai_api_key='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',
        # temperature=1.2,
                #  openai_api_key='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', 
                 model="gpt-4")
retriever = index.vectorstore.as_retriever(search_kwargs={"k": 1})
memory_template = "User: {}<br>ChatGPT: {}<br>"
ENTITY_MEMORY_CONVERSATION_TEMPLATE = ""

# If memory is not empty, reconstruct the conversation template
if st.session_state.entity_memory:
    for entry in st.session_state.entity_memory:
        ENTITY_MEMORY_CONVERSATION_TEMPLATE += memory_template.format(entry["user"], entry["response"])

# Create the conversation chain
Conversation = ConversationChain(
    llm=llm,
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=st.session_state.entity_memory
)

# Streamlit app
st.title("ChatGPT with Memory")

# Get user input
user_input = st.text_input("You:", "")

if st.button("Send"):
    # Add user input to memory
    st.session_state.entity_memory.append({"user": user_input, "response": ""})

    # Generate ChatGPT response
    chatgpt_response = Conversation.generate_response(user_input)

    # Display ChatGPT response
    st.write(f"ChatGPT: {chatgpt_response}")

    # Update memory with ChatGPT response
    st.session_state.entity_memory[-1]["response"] = chatgpt_response
