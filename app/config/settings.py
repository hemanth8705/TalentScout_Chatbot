import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

TOPICS = ["Full Stack Development", "Data Science"]

llm = ChatGroq(
    model="Gemma2-9b-It",
    groq_api_key=os.getenv("GROQ_API_KEY")
)
