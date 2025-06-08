import streamlit as st
import uuid
import json

from utils.detailsValidation import (
    validate_name, validate_email, validate_phone,
    validate_dob, validate_experience,
    validate_department, validate_programming_languages,
    validate_frameworks,
)
from utils.UserDetailsGreetings import (
    greet_initial, greet_user, acknowledge_email,
    acknowledge_phone, comment_on_experience,
    acknowledge_frameworks,
)
from services.candidateRepository import upsert_candidate
from workflows.interviewFlow import run_interview

# ——————————————————————————————
# Session Setup
# ——————————————————————————————
if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4().hex
    upsert_candidate(
        st.session_state.session_id,
        "session_id",
        st.session_state.session_id
    )

if "current_step" not in st.session_state:
    st.session_state.current_step = "name"
    st.session_state.candidate = {}
    st.session_state.messages = []

def add_message(role, text):
    st.session_state.messages.append({"role": role, "content": text})

# ——————————————————————————————
# Initial Greeting (only once)
# ——————————————————————————————
if not st.session_state.messages:
    add_message("assistant", greet_initial())
    add_message("assistant", "👋 Hey there! To get started, what’s your name?")

# ——————————————————————————————
# Render Chat History
# ——————————————————————————————
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

step = st.session_state.current_step
data = st.session_state.candidate

# ——————————————————————————————
# Widget Steps (department, languages, frameworks)
# These appear BEFORE the chat_input below
# ——————————————————————————————
if step == "department":
    dept = st.selectbox(
        "Select the role you are applying for:",
        ["Full Stack", "Frontend", "Backend", "UI/UX", "Data Scientist"],
        key="dept_widget"
    )
    if st.button("OK", key="dept_ok"):
        add_message("user", dept)
        data["department"] = dept
        upsert_candidate(st.session_state.session_id, "department", dept)
        add_message("assistant", f"Great! You’re applying for **{dept}**.")
        add_message("assistant", "Next up: select your programming languages.")
        st.session_state.current_step = "languages"
        st.experimental_rerun()

elif step == "languages":
    langs = st.multiselect(
        "Select your Programming Languages:",
        ["Python", "JavaScript", "Java", "C++", "Go", "Ruby"],
        key="langs_widget"
    )
    if st.button("OK", key="langs_ok"):
        add_message("user", ", ".join(langs))
        data["programming_languages"] = langs
        upsert_candidate(
            st.session_state.session_id,
            "programming_languages",
            langs
        )
        add_message("assistant", f"Awesome—{', '.join(langs)}.")
        add_message("assistant", "Now pick any frameworks you know (optional).")
        st.session_state.current_step = "frameworks"
        st.experimental_rerun()

elif step == "frameworks":
    frameworks = st.multiselect(
        "Select frameworks you know (optional):",
        ["Django", "Flask", "React", "Angular", "Vue", "Spring"],
        key="fw_widget"
    )
    if st.button("OK", key="fw_ok"):
        add_message("user", ", ".join(frameworks) or "None")
        data["frameworks"] = frameworks
        upsert_candidate(
            st.session_state.session_id,
            "frameworks",
            frameworks
        )
        add_message("assistant", acknowledge_frameworks(frameworks))
        add_message("assistant", "Great—I'm all set to generate your technical questions!")
        st.session_state.current_step = "final"
        st.experimental_rerun()

# ——————————————————————————————
# Chat-Style Free-Form Steps
# Only render chat_input if not in a widget step
# ——————————————————————————————
elif step not in ["department", "languages", "frameworks"]:
    user_input = st.chat_input("Type your response here…", key="chat_input")

    if user_input:
        add_message("user", user_input)

        if step == "name":
            if validate_name(user_input):
                data["name"] = user_input
                upsert_candidate(st.session_state.session_id, "name", user_input)
                add_message("assistant", greet_user(user_input))
                add_message("assistant", "Thanks! What’s your email address?")
                # st.session_state.current_step = "email"
                st.session_state.current_step = "final"  # Skip to final step for demo
            else:
                add_message("assistant", "❗️ Name must be alphabetic and ≥2 chars.")

        elif step == "email":
            if validate_email(user_input):
                data["email"] = user_input
                upsert_candidate(st.session_state.session_id, "email", user_input)
                add_message("assistant", acknowledge_email(user_input))
                add_message("assistant", "Perfect. May I have your phone number next?")
                st.session_state.current_step = "phone"
            else:
                add_message("assistant", "❗️ Please enter a valid email.")

        elif step == "phone":
            if validate_phone(user_input):
                data["phone"] = user_input
                upsert_candidate(st.session_state.session_id, "phone", user_input)
                add_message("assistant", acknowledge_phone())
                add_message("assistant", "Thanks! Now enter your date of birth (YYYY-MM-DD).")
                st.session_state.current_step = "dob"
            else:
                add_message("assistant", "❗️ Phone must be 10–15 digits.")

        elif step == "dob":
            if validate_dob(user_input):
                data["dob"] = user_input
                upsert_candidate(st.session_state.session_id, "dob", user_input)
                add_message("assistant", "Got it!")
                add_message("assistant", "How many years of experience do you have?")
                st.session_state.current_step = "experience"
            else:
                add_message("assistant", "❗️ DOB must be YYYY-MM-DD and you must be over 18.")

        elif step == "experience":
            try:
                exp = float(user_input)
                if validate_experience(exp):
                    data["years_experience"] = exp
                    upsert_candidate(
                        st.session_state.session_id,
                        "years_experience",
                        exp
                    )
                    add_message("assistant", comment_on_experience(exp))
                    add_message("assistant", "Which department are you applying for? (e.g., Full Stack)")
                    st.session_state.current_step = "department"
                else:
                    raise ValueError
            except:
                add_message("assistant", "❗️ Enter a valid number ≥0 for years of experience.")

        st.experimental_rerun()

# ——————————————————————————————
# Final Step & “Start Interview”
# ——————————————————————————————
if step == "final":
    add_message("assistant",
        f"Thanks {data['name']}! Getting your technical questions ready…")
    st.write("### Candidate Summary")
    st.json(data)

    if st.button("Start Interview"):
        subjects = ["Full Stack", "Data Science"]  # or derive from data["department"]
        results = run_interview(subjects, {})
        st.session_state.interview_results = results
        st.session_state.interview_subject_idx = 0
        st.session_state.interview_question_idx = 0

        st.session_state.current_step = "interview"
        st.experimental_rerun()

# ——————————————————————————————
# Interview Placeholder
# ——————————————————————————————
elif step == "interview":
    subjects = list(st.session_state.interview_results.keys())
    s_idx = st.session_state.interview_subject_idx
    q_idx = st.session_state.interview_question_idx

    # Finished all subjects?
    if s_idx >= len(subjects):
        add_message("assistant", "🎉 Interview complete! Here’s your summary:")
        add_message("assistant", json.dumps(st.session_state.interview_results, indent=2))
        st.session_state.current_step = "done"
        st.experimental_rerun()

    subject = subjects[s_idx]
    qa_list = st.session_state.interview_results[subject]["questions"]

    # Check if current subject's questions are done.
    if q_idx >= len(qa_list):
        # Move on to next subject:
        st.session_state.interview_subject_idx += 1
        st.session_state.interview_question_idx = 0
        st.experimental_rerun()

    ideal = qa_list[q_idx]["ideal_answer"]
    question = qa_list[q_idx]["question"]

    # 1) Persist the question
    add_message("assistant", f"**[{subject}] Q{q_idx+1}:** {question}")

    # 2) Show full chat
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # 3) Capture answer
    answer = st.chat_input("Your answer…", key=f"ans_{subject}_{q_idx}")
    if answer:
        add_message("user", answer)
        st.session_state.interview_results[subject]["answers"].append(answer)

        # 4) Evaluate & persist
        from services.interviewEngine import evaluate_answer
        fb = evaluate_answer(question, ideal, answer)
        add_message("assistant", fb)
        st.session_state.interview_results[subject]["feedback"].append(fb)

        # 5) Move on
        st.session_state.interview_question_idx += 1
        st.experimental_rerun()


# ——————————————————————————————
# Global “Start Over”
# ——————————————————————————————
if st.button("Start Over"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.experimental_rerun()
