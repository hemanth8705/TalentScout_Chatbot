from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from config.settings import llm
from prompts.interviewPrompt import make_prompt_template
from memory.sessionMemory import get_session_history
from utils.trimmer import trimmer

prompt = make_prompt_template()

trimmed_chain = (
    RunnablePassthrough.assign(
        messages=itemgetter("messages") | trimmer
    )
    | prompt
    | llm
)

chat = RunnableWithMessageHistory(
    trimmed_chain,
    get_session_history,
    input_messages_key="messages"
)
