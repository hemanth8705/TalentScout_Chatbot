import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from chains.ChatChain import chat
from memory.sessionMemory import get_session_history
from utils.trimmer import trimmer

# Keys to collect, in order
PROFILE_FIELDS = [
    "Full Name", "Email Address", "Phone Number",
    "Years of Experience", "Desired Position(s)",
    "Current Location", "Tech Stack"
]


# --- Streamlit UI ---
st.set_page_config(page_title="Dynamic Interview Bot", page_icon="🤖")
st.title("🧠 Dynamic Interview Coach")


if "session_id" not in st.session_state:
    st.session_state.session_id = "candidate_001"

if "messages" not in st.session_state:
    st.session_state.messages   = []
    st.session_state.profile    = {f: None for f in PROFILE_FIELDS}
    st.session_state.field_idx  = 0
    st.session_state.collecting = True
    # Kick off with first question
    first_q = f"Hey there! Let’s get you set up. What’s your **{PROFILE_FIELDS[0]}**?"
    st.session_state.messages.append({"role": "assistant", "content": first_q})

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

config = {"configurable": {"session_id": st.session_state.session_id}}




if user_input := st.chat_input("Your answer..."):  # same input
    # — append & display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    if st.session_state.collecting:
        # capture profile field
        field = PROFILE_FIELDS[st.session_state.field_idx]
        if field == "Tech Stack":
            tech_list = [tech.strip() for tech in user_input.split(',') if tech.strip()]
            st.session_state.profile[field] = tech_list
        else:
            st.session_state.profile[field] = user_input.strip()
        st.session_state.field_idx += 1

        # decide next step
        if st.session_state.field_idx < len(PROFILE_FIELDS):
            next_f = PROFILE_FIELDS[st.session_state.field_idx]
            bot_msg = f"Cool, now enter your **{next_f}**:"
        else:
            # done collecting
            st.session_state.collecting = False
            summary = "\n".join(
                f"**{k}**: {v}" for k, v in st.session_state.profile.items()
            )
            tech_stack = st.session_state.profile["Tech Stack"]
            bot_msg = (
                "All set! Here's what I got:\n\n"
                f"{tech_stack}\n\nLet’s dive into the interview! 🤖💬"
            )

            # append & display the bot message
            st.session_state.messages.append({"role": "assistant", "content": bot_msg})
            st.chat_message("assistant").markdown(bot_msg)

            
            # prime the LLM for the interview
            resp = chat.invoke({"messages": []}, config=config)
            st.session_state.messages.append({
                "role": "assistant", "content": resp.content
            })
            # immediately render that LLM greeting below
            st.chat_message("assistant").markdown(resp.content)

        
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})

        full_history = get_session_history(st.session_state.session_id).messages
        trimmed_history = trimmer.invoke(full_history)
        messages = list(trimmed_history)

        if sum(1 for m in full_history if isinstance(m, HumanMessage)) == 2:
            print("Switching topics...")
            messages.append(SystemMessage(content="Switch to hard-level Python interview questions now."))

        messages.append(HumanMessage(content=user_input))
        bot_resp = chat.invoke({"messages": messages}, config=config)

        st.chat_message("assistant").markdown(bot_resp.content)
        st.session_state.messages.append({"role": "assistant", "content": bot_resp.content})
