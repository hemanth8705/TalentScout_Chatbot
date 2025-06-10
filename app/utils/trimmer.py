from langchain_core.messages import trim_messages
from config.settings import llm

trimmer = trim_messages(
    max_tokens=4500,
    strategy="last",
    token_counter=llm,
    include_system=True,
    allow_partial=False,
    start_on="human"
)
