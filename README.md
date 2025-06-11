# TalentScout Hiring Chatbot

## Project Overview
TalentScout Hiring Chatbot is an interactive interview assistant designed to guide candidates through a dynamic interview process. The chatbot collects candidate details, validates the input, and conducts interviews tailored to the candidate's technology stack. The app features a modern, WhatsApp-like user interface for a seamless conversational experience.

## Installation Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/hemanth8705/TalentScout_Chatbot.git
   cd TalentScout_Chatbot
   ```

2. **Create and Activate the Virtual Environment (Windows):**
   ```bash
   python -m venv langchain_venv
   langchain_venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   - Create a `.env` file in the `app/` directory.
   - Add the required API keys (e.g., `GROQ_API_KEY`).

5. **Run the Application:**
   ```bash
   streamlit run app/ui.py
   ```

## LINKS
- [ ]  Demo walkthrough video in loom : [Demo Video Link](https://www.loom.com/share/6fac0fbdb91f47948238815185f2dcce?sid=e19f45e0-3ad3-4dff-b395-d7e3b10c3df6)

- [ ]  Live version link: [Live App Link](https://talentscout-chatbot-gvmu.onrender.com)
- [ ]  Documentation link: [Project Documentation](https://docs.google.com/document/d/11r449IiRCukmyFMcoc84GyCgerUSo62hz8VwvGUnBJ4)

## Usage Guide
- When the application starts, the candidate is greeted and prompted to provide personal and technical details.
- Input is validated using custom validation functions. Invalid entries prompt an immediate error message.
- Once details are collected, the chatbot starts the interview by asking tailored technical questions.
- The conversation is displayed in a clean, WhatsApp-like chat interface:
  - **Bot messages:** Aligned to the left.
  - **User messages:** Aligned to the right.
- Typing keywords like “exit” or “quit” triggers a strict prompt to conclude the interview, providing a professional evaluation summary before ending the session.

## Technical Details
- **Front-End:** Streamlit for UI rendering.
- **Back-End:** Python integrating the LangChain framework with ChatGroq.
- **Key Libraries:**
  - streamlit
  - python-dotenv
  - langchain-groq
  - langchain-core
  - langchain-community
- **Architecture:**
  - **UI Component:** `app/ui.py`
  - **Chat Chain:** `app/chains/ChatChain.py`
  - **Prompt Template:** `app/prompts/interviewPrompt.py`
  - **Memory Management:** `app/memory/sessionMemory.py`
  - **Utilities:** 
    - Validation logic in `app/utils/detailsValidation.py`
    - Message and token trimming in `app/utils/trimmer.py`
    - Custom greetings in `app/utils/UserDetailsGreetings.py`

## Prompt Design
- The chatbot uses strict prompt templates to ensure consistent LLM responses.
- Prompts are crafted to handle:
  - **Information Gathering:** Collecting candidate details with validations.
  - **Technical Question Generation:** Generating context-specific, follow-up questions.
  - **Interview Termination:** When exit keywords are detected, a dedicated strict prompt instructs the LLM to provide an evaluation summary and conclude the session without extra commentary.

## Challenges & Solutions
- **Persistent Token Accumulation:**
  - **Issue:** In production, session state and token counts were not resetting on page refresh.
  - **Solution:** Explicitly cleared `st.session_state` on app load to ensure a fresh session each time.
- **UI Inconsistencies:**
  - **Issue:** Default emoji-based chat messages resulted in flickers and misalignment.
  - **Solution:** Injected custom CSS to render messages in a WhatsApp-like style, aligning bot messages to the left and user messages to the right.
- **Message History Management:**
  - **Issue:** LLM responses were not being consistently appended, causing chat history to vanish.
  - **Solution:** Ensured that every LLM response is recorded in `st.session_state.messages` and rendered uniformly.
- **Input Validation:**
  - **Issue:** Inconsistent candidate information.
  - **Solution:** Developed robust validation functions to check inputs (e.g., name, email, phone, experience) before moving ahead.

## Final Feature Checklist ✅ Hiring Assistant Chatbot

---

#### 🖥️ **UI Implementation (Streamlit/Gradio)**
- ✅ Clean and intuitive chatbot UI built using **Streamlit** or **Gradio**
- ✅ Greeting message with chatbot purpose (on startup)
- ✅ Exit capability on keywords like "bye", "quit", "exit", etc.

---

#### 💬 **Chatbot Functionalities**
- ✅ Collect Full Name
- ✅ Collect Email Address
- ✅ Collect Phone Number
- ✅ Collect Years of Experience
- ✅ Collect Desired Position(s)
- ✅ Collect Current Location
- ✅ Collect Tech Stack: programming languages, frameworks, DBs, tools
- ✅ Store all the above in a structured format (dict, JSON, etc.)

---

#### 🧠 **LLM Prompting & Context Handling**
- ✅ Use an LLM (GPT-3.5 / GPT-4 / Groq / llama2 / etc.)
- ✅ Prompt candidate to declare tech stack clearly
- ✅ Generate **3–5 technical questions** per declared tech skill  
  - 🔁 Bonus if dynamically generated (not hardcoded)
- ✅ Maintain **conversational context** across turns (e.g. follow-ups)
- ✅ Handle irrelevant or unexpected inputs with fallback replies
- ✅ Don’t allow LLM to drift from interview topic (guardrails)
- ✅ Graceful ending: Thank candidate + mention next steps

---

#### 🔐 **Data Handling & Privacy**
- ✅ Use **simulated data** (not real candidate info)
- ✅ No actual PII stored unless anonymized
- ✅ Ensure flow aligns with **GDPR-like** practices
- ✅ Clearly mention privacy measures in README

---

#### 📦 **Tech Stack**
- ✅ Language: **Python**
- ✅ Tools: Streamlit, LangChain/OpenAI API/Groq API/etc.
- ✅ Optional: LangChain memory management (`RunnableWithMessageHistory`)

---

#### 🚀 **Deployment**
- ✅ Local Deployment 
- ✅  BONUS: Deployed on cloud (GCP, AWS, etc.)
- ✅  BONUS: Live demo link (Loom video, or public link)

---

#### 📄 **README & Documentation Checklist**
- ✅ Project Overview: Brief summary of chatbot
- ✅ Setup Instructions: Install requirements, run the app
- ✅ Usage Guide: How to use the chatbot
- ✅ Technical Details: Libraries, models, architecture used
- ✅ Prompt Design Explanation
- ✅ Challenges Faced + Solutions
- ✅ Clear, concise formatting + structure

---

#### 🔁 **Code Quality Checklist**
- ✅ Modular structure (functions/classes split by logic)
- ✅ Proper docstrings + inline comments
- ✅ Clean and readable variable names
- ✅ Git version control used (no last-minute dumping code!)
- ✅ Clear commit history (avoid "finalfinal-final.py" stuff 😅)

---

#### ⭐ **Optional Enhancements (Bonus Points Zone)**
- ✅ Sentiment Analysis during chat
- ✅ Multilingual support (basic language switch at least)
- ✅ Personalized responses based on previous answers
- ✅ Custom-styled Streamlit UI (CSS injection / components)
- ✅ Performance: Fast response handling, async where needed

---

#### 🧪 **Testing & Final Validation**
- ✅ Run end-to-end flow at least 3x to test edge cases
- ✅ Test fallback handling (random garbage inputs)
- ✅ Confirm conversation-ending keywords work
- ✅ Validate all inputs are correctly stored + displayed

---

#### 📤 **Final Deliverables**
- ✅  Public GitHub repo or ZIP file
- ✅  README completed
- ✅  (Bonus) Loom / demo walkthrough video
- ✅  Submit via Career Page

## Conclusion
TalentScout Hiring Chatbot offers a modern, engaging approach to candidate interviews by combining advanced LLM capabilities with a user-friendly interface. Its design ensures efficient data collection, precise evaluation, and a consistent, professional interview flow.

Happy Hiring!