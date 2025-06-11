import streamlit as st
from chains.ChatChain import chat
import random
from utils.detailsValidation import validate_name, validate_email, validate_phone, validate_experience, validate_programming_languages
import logging


# --- Configure Logger ---
log_format = "%(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))

file_handler = logging.FileHandler("app.log", mode='a')
file_handler.setFormatter(logging.Formatter(log_format))

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# --- Streamlit UI ---
st.set_page_config(page_title="TalentScout Hiring Bot", page_icon="🤖")
st.title("🧠 TalentScout Hiring Bot")


#  Inject custom CSS
st.markdown(
    """
    <style>
    /* Wrapper to align messages */
    .bot-wrapper {
        text-align: left;
        width: 100%;
    }
    .user-wrapper {
        text-align: right;
        width: 100%;
    }
    /* Chat message styles that shrink to fit content */
    .bot-message, .user-message {
        display: inline-block;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 70%;
    }
    .bot-message {
        background-color: #f0f2f6;
    }
    .user-message {
        background-color: #d1e7dd;
    }
    </style>
    """,
    unsafe_allow_html=True
    
)

logger.info("Custom CSS injected.")


# Keys to collect, in order
PROFILE_FIELDS = [
    "Full Name", "Email Address", "Phone Number",
    "Years of Experience", "Desired Position(s)",
    "Current Location", "Tech Stack"
]



st.session_state.session_id = "candidate_001"

if "messages" not in st.session_state:
    st.session_state.messages   = []
    st.session_state.profile    = {f: None for f in PROFILE_FIELDS}
    st.session_state.field_idx  = 0
    st.session_state.collecting = True
    # Kick off with first question for profile field collection
    first_q = f"Hey there! Let’s get you set up. What’s your {PROFILE_FIELDS[0]}?"
    st.session_state.messages.append({"role": "assistant", "content": first_q})
    logger.info("Session state initialized. First question: %s", first_q)

# Display chat history

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(f'<div class="bot-wrapper"><div class="bot-message">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-wrapper"><div class="user-message">{msg["content"]}</div></div>', unsafe_allow_html=True)

logger.info("Rendered chat history with %d messages.", len(st.session_state.messages))


config = {"configurable": {"session_id": st.session_state.session_id}}

if user_input := st.chat_input("Your answer..."):

    st.session_state.messages.append({"role": "user", "content": user_input})
    # st.chat_message("user").markdown(user_input)
    st.markdown(f'<div class="user-wrapper"><div class="user-message">{user_input}</div></div>', unsafe_allow_html=True)
    logger.info("User input received: %s", user_input)

        # Check for quit keywords
    if user_input.lower().strip() in ("exit", "quit"):
        exit_prompt = (
            "The user has requested to end the interview.\n\n"
            "You are required to strictly follow these instructions without any deviation or additional commentary:\n\n"
            "1. Conclude the interview immediately.\n"
            "2. Provide a concise, professional evaluation summary of the interview so far.\n"
            "3. Thank the candidate for their time and bid them goodbye.\n\n"
            "IMPORTANT: Respond ONLY with the evaluation summary and goodbye message. DO NOT include any extra context, apologies, or remarks."
        )
        logger.info("User requested to end interview. Triggering exit prompt.")
        resp = chat.invoke({"prompt": exit_prompt, "messages": st.session_state.messages}, config=config)
        st.session_state.messages.append({"role": "assistant", "content": resp.content})
        st.markdown(f'<div class="bot-wrapper"><div class="bot-message">{resp.content}</div></div>', unsafe_allow_html=True)
        logger.info("LLM termination response: %s", resp.content)
        st.stop()  # End the app execution

    if st.session_state.collecting:
        field = PROFILE_FIELDS[st.session_state.field_idx]
        is_valid = True
        error_msg = ""

        logger.info("Validating field: %s", field)
        if field == "Full Name":
            if not validate_name(user_input):
                is_valid = False
                error_msg = ("Invalid Full Name. Please enter a valid name using alphabetic characters only "
                             "and ensure it is at least 2 characters long.")
        elif field == "Email Address":
            if not validate_email(user_input):
                is_valid = False
                error_msg = "Invalid Email Address. Please enter a valid email address."
        elif field == "Phone Number":
            if not validate_phone(user_input):
                is_valid = False
                error_msg = ("Invalid Phone Number. Please enter a valid phone number containing only digits "
                             "and between 10 and 15 characters.")
        elif field == "Years of Experience":
            try:
                exp = float(user_input)
                if not validate_experience(exp):
                    is_valid = False
                    error_msg = "Invalid Years of Experience. Must be a non-negative number."
                else:
                    user_input = exp
            except Exception:
                is_valid = False
                error_msg = "Invalid Years of Experience. Please enter a valid number."
        elif field == "Tech Stack":
            tech_list = [tech.strip() for tech in user_input.split(',') if tech.strip()]
            if not validate_programming_languages(tech_list):
                is_valid = False
                error_msg = ("Invalid Tech Stack. Please enter one or more valid programming languages or technologies.")
            else:
                user_input = tech_list
        # For other fields (Desired Position(s), Current Location) no validation is applied

        if not is_valid:
            st.error(error_msg)
            logger.warning("Validation failed for field '%s' with error: %s", field, error_msg)
        else:
            # Save the validated input and advance to next field
            st.session_state.profile[field] = user_input
            st.session_state.field_idx += 1
            logger.info("Validated field '%s'. Updated profile.", field)

            # Decide next step for profile collection
            if st.session_state.field_idx < len(PROFILE_FIELDS):
                next_f = PROFILE_FIELDS[st.session_state.field_idx]
                bot_msg = f"Cool, now enter your {next_f}:"
                st.session_state.messages.append({"role": "assistant", "content": bot_msg})
                st.markdown(f'<div class="bot-wrapper"><div class="bot-message">{bot_msg}</div></div>', unsafe_allow_html=True)
                logger.info("Prompting next field: %s", next_f)
            else:
                st.session_state.collecting = False
                # Immediately greet the user and ask the first interview question
                greeting = "Great! Preparing your interview based on your selected tech stack..."
                st.session_state.messages.append({"role": "assistant", "content": greeting})
                st.markdown(f'<div class="bot-wrapper"><div class="bot-message">{greeting}</div></div>', unsafe_allow_html=True)
                logger.info("Profile completed. %s", greeting)


                # Initialize interview state
                tech_stack = st.session_state.profile["Tech Stack"]
                st.session_state.tech_topic_index = 0
                st.session_state.topic_question_count = 0
                st.session_state.current_topic_threshold = random.randint(2, 3)
                current_topic = tech_stack[st.session_state.tech_topic_index]
                # Define first interview question for the first tech topic (customize as needed)
                prompt = (
                    f"The topic is: {current_topic}\n"
                    "Start the interview by asking an introductory question about this topic.\n"
                    "Do not wait for any previous answers. This is the first question of the interview.\n"
                    "Keep it relevant and conversational."
                )
                logger.info("Initializing interview for topic: %s", current_topic)
                resp = chat.invoke(
                        {"prompt": prompt, "messages": st.session_state.messages},
                        config=config
                    )
                st.session_state.messages.append({"role": "assistant", "content": resp.content})
                st.markdown(f'<div class="bot-wrapper"><div class="bot-message">{resp.content}</div></div>', unsafe_allow_html=True)
                st.session_state.last_question = resp.content
                logger.info("LLM response received for initial interview question. Response: %s", resp.content)
    else:
        # Interview phase using a single prompt string
        tech_stack = st.session_state.profile["Tech Stack"]
        current_topic = (
            tech_stack[st.session_state.tech_topic_index]
            if st.session_state.tech_topic_index < len(tech_stack) and isinstance(tech_stack, list)
            else "general topics"
        )
        
        st.session_state.topic_question_count += 1

        if st.session_state.topic_question_count >= st.session_state.current_topic_threshold:
            if st.session_state.tech_topic_index < len(tech_stack) - 1:
                next_topic = tech_stack[st.session_state.tech_topic_index + 1]
                prompt = (
                    f"Current topic '{current_topic}' is completed. Please wrap up by summarizing your feedback for the candidate’s last answer:\n"
                    f"User's answer: {user_input}\n"
                    f"Then, switch the conversation to the next topic: {next_topic}.\n"
                    f"Finally, ask the candidate an introductory question for {next_topic}."
                )
                logger.info("Switching to next topic: %s", next_topic)
                resp = chat.invoke(
                    {"prompt": prompt, "messages": st.session_state.messages},
                    config=config
                )
                st.session_state.messages.append({"role": "assistant", "content": resp.content})
                st.markdown(f'<div class="bot-wrapper"><div class="bot-message">{resp.content}</div></div>', unsafe_allow_html=True)
                st.session_state.tech_topic_index += 1
                st.session_state.topic_question_count = 0
                st.session_state.current_topic_threshold = random.randint(2, 3)
                st.session_state.last_question = resp.content
                logger.info("LLM response for topic switch: %s", resp.content)
            else:
                prompt = (
                    "All topics have been covered.\n\n"
                    "You are required to strictly follow these instructions without any deviation or additional commentary:\n\n"
                    "1. Synthesize an objective evaluation summary of the entire interview process using the chat history.\n"
                    "2. Provide a brief, clear, and unambiguous summary that highlights the candidate's strengths and areas for improvement.\n"
                    "3. End the interview by thanking the candidate in a concise manner, explicitly stating that the interview is concluded.\n\n"
                    "IMPORTANT: Respond ONLY with the interview evaluation summary and the thank-you message. DO NOT include any extra context, apologies, or remarks."
                )
                logger.info("All topics completed, summarizing interview.")
                resp = chat.invoke(
                    {"prompt": prompt, "messages": st.session_state.messages},
                    config=config
                )
                st.session_state.messages.append({"role": "assistant", "content": resp.content})
                st.markdown(f'<div class="bot-wrapper"><div class="bot-message">{resp.content}</div></div>', unsafe_allow_html=True)
                logger.info("LLM summary response: %s", resp.content)
        else:
            prompt = (
                f"Here is the question: {st.session_state.last_question}\n"
                f"User's answer: {user_input}\n\n"
                "You are required to strictly follow these instructions without any deviation or additional commentary:\n\n"
                "1. Evaluate the user's answer and determine if it is relevant, correct, and complete.\n"
                "2. Provide a brief, clear, and unambiguous evaluation of the answer.\n"
                "3. If the answer is correct:\n   - Ask a follow-up question that dives deeper into the same topic.\n"
                "4. If the answer is incorrect:\n   - Provide corrective feedback and ask a simplified follow-up question centered on the same topic.\n\n"
                "IMPORTANT: Respond ONLY with the evaluation and the follow-up question. DO NOT include any extra context, apologies, or additional remarks."
            )
            logger.info("In normal interview phase. Current topic: %s | Last question: %s | User input: %s", current_topic, st.session_state.last_question, user_input)

            resp = chat.invoke(
                    {"prompt": prompt, "messages": st.session_state.messages},
                    config=config
                )
            st.session_state.messages.append({"role": "assistant", "content": resp.content})
            st.markdown(f'<div class="bot-wrapper"><div class="bot-message">{resp.content}</div></div>', unsafe_allow_html=True)
            st.session_state.last_question = resp.content
            logger.info("LLM response in normal phase: %s", resp.content)