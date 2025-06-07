import streamlit as st
import json
import uuid
from utils.detailsValidation import (
    validate_name,
    validate_email,
    validate_phone,
    validate_dob,
    validate_experience,
    validate_department,
    validate_programming_languages,
    validate_frameworks,
)

# Add to the existing import block in ui.py
from utils.UserDetailsGreetings import (
    greet_initial,
    greet_user,
    acknowledge_email,
    acknowledge_phone,
    comment_on_experience,
    acknowledge_frameworks,
)

from services.candidateRepository import upsert_candidate

# Initialize session state variables if not present
if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4().hex
    # Save session_id into DB so we can upsert subsequent fields
    upsert_candidate(st.session_state.session_id, "session_id", st.session_state.session_id)

if "current_step" not in st.session_state:
    st.session_state.current_step = "name"
    st.session_state.candidate = {}
    st.session_state.messages = []

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Conversational flow based on current_step
if st.session_state.current_step == "name":
    # On first visit, greet the user.
    if not st.session_state.messages:
        add_message("assistant", greet_initial())
        st.experimental_rerun()
    name_input = st.text_input("Enter your name:", key="name_input")
    if st.button("Submit Name"):
        if validate_name(name_input):
            add_message("user", name_input)
            st.session_state.candidate["name"] = name_input
            upsert_candidate(st.session_state.session_id, "name", name_input)
            add_message("assistant", greet_user(name_input))
            st.session_state.current_step = "email"
            st.experimental_rerun()
        else:
            st.error("Please enter a valid name (alphabetic characters only, at least 2 characters).")

elif st.session_state.current_step == "email":
    email_input = st.text_input("Enter your email:", key="email_input")
    if st.button("Submit Email"):
        if validate_email(email_input):
            add_message("user", email_input)
            st.session_state.candidate["email"] = email_input
            upsert_candidate(st.session_state.session_id, "email", email_input)
            add_message("assistant", acknowledge_email(email_input))
            st.session_state.current_step = "phone"
            st.experimental_rerun()
        else:
            st.error("Please enter a valid email address.")

elif st.session_state.current_step == "phone":
    phone_input = st.text_input("Enter your phone number:", key="phone_input")
    if st.button("Submit Phone"):
        if validate_phone(phone_input):
            add_message("user", phone_input)
            st.session_state.candidate["phone"] = phone_input
            upsert_candidate(st.session_state.session_id, "phone", phone_input)
            add_message("assistant", acknowledge_phone())
            st.session_state.current_step = "dob"
            st.experimental_rerun()
        else:
            st.error("Please enter a valid phone number (digits only, 10-15 characters).")

elif st.session_state.current_step == "dob":
    dob_input = st.text_input("Enter your Date of Birth (YYYY-MM-DD):", key="dob_input")
    if st.button("Submit DOB"):
        if validate_dob(dob_input):
            add_message("user", dob_input)
            st.session_state.candidate["dob"] = dob_input
            upsert_candidate(st.session_state.session_id, "dob", dob_input)
            add_message("assistant", "Got it.")
            st.session_state.current_step = "experience"
            st.experimental_rerun()
        else:
            st.error("Please enter a valid DOB (format YYYY-MM-DD) and ensure you are over 18.")

elif st.session_state.current_step == "experience":
    exp_input = st.number_input("Enter years of experience:", min_value=0, step=1, key="exp_input")
    if st.button("Submit Experience"):
        if validate_experience(exp_input):
            add_message("user", str(exp_input))
            st.session_state.candidate["years_experience"] = exp_input
            upsert_candidate(st.session_state.session_id, "years_experience", exp_input)
            add_message("assistant", comment_on_experience(exp_input))
            st.session_state.current_step = "department"
            st.experimental_rerun()
        else:
            st.error("Please enter a valid number for years of experience (0 or greater).")

elif st.session_state.current_step == "department":
    dept_input = st.selectbox(
        "Select the role you are applying for:",
        options=["Full Stack", "Frontend", "Backend", "UI/UX", "Data Scientist"],
        key="dept_input"
    )
    if st.button("Submit Department"):
        if dept_input and validate_department(dept_input):
            add_message("user", dept_input)
            st.session_state.candidate["department"] = dept_input
            upsert_candidate(st.session_state.session_id, "department", dept_input)
            add_message("assistant", f"Great! You are applying for the {dept_input} role.")
            st.session_state.current_step = "languages"
            st.experimental_rerun()
        else:
            st.error("Please select a valid department.")

elif st.session_state.current_step == "languages":
    langs_input = st.multiselect(
        "Select your Programming Languages:",
        options=["Python", "JavaScript", "Java", "C++", "Go", "Ruby"],
        key="langs_input"
    )
    if st.button("Submit Languages"):
        if langs_input and validate_programming_languages(langs_input):
            add_message("user", ", ".join(langs_input))
            st.session_state.candidate["programming_languages"] = langs_input
            upsert_candidate(st.session_state.session_id, "programming_languages", langs_input)
            add_message("assistant", f"Great! You have experience in {', '.join(langs_input)}.")
            st.session_state.current_step = "frameworks"
            st.experimental_rerun()
        else:
            st.error("Please select at least one programming language.")

elif st.session_state.current_step == "frameworks":
    frameworks_input = st.multiselect(
        "Select the frameworks you know (optional):",
        options=["Django", "Flask", "React", "Angular", "Vue", "Spring"],
        key="frameworks_input"
    )
    if st.button("Submit Frameworks"):
        if validate_frameworks(frameworks_input):
            frameworks_val = ", ".join(frameworks_input) if frameworks_input else "None"
            add_message("user", frameworks_val)
            st.session_state.candidate["frameworks"] = frameworks_input
            upsert_candidate(st.session_state.session_id, "frameworks", frameworks_input)
            add_message("assistant", acknowledge_frameworks(frameworks_input))
            st.session_state.current_step = "final"
            st.experimental_rerun()
        else:
            st.error("Please enter valid frameworks (non-empty strings).")

elif st.session_state.current_step == "final":
    add_message("assistant", f"Thanks {st.session_state.candidate.get('name', 'User')}! Your information is noted. I’ll now prepare your technical questions.")
    st.write("Candidate Data:")
    st.json(st.session_state.candidate)
    if st.button("Start Over"):
        # Reset session state for a fresh start.
        for key in ["candidate", "current_step", "messages", "name_input", "email_input", "phone_input",
                    "dob_input", "exp_input", "dept_input", "langs_input", "frameworks_input", "session_id"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()