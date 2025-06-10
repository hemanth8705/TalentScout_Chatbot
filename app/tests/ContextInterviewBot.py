import os
from operator import itemgetter
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, trim_messages
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough

# --- Config & Prompts ---
TOPICS = ["Full Stack Development", "Data Science"]

def make_prompt_template():
    system_msg = f"""
You are a 🔥 dynamic interview coach 🔥 covering these topics: {TOPICS}.

Flow rules:
1. Ask **one** question at a time.
2. After user answers:
   • If correct → ask a deeper/follow-up Q on that topic.
   • If incorrect → simplify/reframe or revisit fundamentals before moving on.
3. **After two** questions in the same topic, switch to the other topic.
5. Keep it conversational & encouraging.

Just output the next question (and any short feedback). Do **not** write any code blocks.
"""
    return ChatPromptTemplate.from_messages([
        ("system", system_msg),
        MessagesPlaceholder(variable_name="messages")
    ])

# --- Memory Store ---
_store: dict[str, ChatMessageHistory] = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = ChatMessageHistory()
    return _store[session_id]

# --- Load LLM ---
load_dotenv()
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=os.getenv("GROQ_API_KEY"))

# --- Token Trimmer ---
trimmer = trim_messages(
    max_tokens=4500,
    strategy="last",
    token_counter=llm,
    include_system=True,
    allow_partial=False,
    start_on="human"
)

# --- Build Chain ---
prompt = make_prompt_template()
raw_chain = prompt | llm
# Insert trimming before prompt
trimmed_chain = (
    RunnablePassthrough.assign(
        messages=itemgetter("messages") | trimmer
    )
    | prompt
    | llm
)

# --- Wrap with Memory ---
chat = RunnableWithMessageHistory(
    trimmed_chain,
    get_session_history,
    input_messages_key="messages"
)

# --- Streamlit UI ---
st.set_page_config(page_title="Dynamic Interview Bot", page_icon="🤖")
st.title("🧠 Dynamic Interview Coach")

if "session_id" not in st.session_state:
    st.session_state.session_id = "candidate_001"

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Kick off with first question
    config = {"configurable": {"session_id": st.session_state.session_id}}
    response = chat.invoke({"messages": []}, config=config)
    st.session_state.messages.append({"role": "assistant", "content": response.content})

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

config = {"configurable": {"session_id": st.session_state.session_id}}
# Handle user input
if user_input := st.chat_input("Your answer..."):
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Fetch full history for logic
    full_history = get_session_history(st.session_state.session_id).messages
    # Trim history for model input
    trimmed_history = trimmer.invoke(full_history)

    messages = list(trimmed_history)
    # Inject system message after two user answers
    if sum(1 for m in full_history if isinstance(m, HumanMessage)) == 2:
        print("Switching topics...")
        messages.append(SystemMessage(content="Switch to hard-level Python interview questions now."))

    # Add current user turn
    messages.append(HumanMessage(content=user_input))

    # Invoke the chat model
    bot_resp = chat.invoke({"messages": messages}, config=config)

    # Display bot response
    st.chat_message("assistant").markdown(bot_resp.content)
    st.session_state.messages.append({"role": "assistant", "content": bot_resp.content})

