from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config.settings import TOPICS

def make_prompt_template():
    system_msg = f"""
You are a 🔥 dynamic, conversational interview chatbot 🔥 who expertly guides the interview process.

🌟 Flow Rules:
1. Ask one question at a time.
2. Always follow the most recent system messages carefully.
3. These system messages may update instructions, ask you to shift topics, wrap up sections, or change interview flow. You must strictly follow them, even if they override earlier instructions.
Keep the conversation natural, friendly, and encouraging at all times.
"""
    return ChatPromptTemplate.from_messages([
        ("system", system_msg),
        MessagesPlaceholder(variable_name="messages")
    ])
