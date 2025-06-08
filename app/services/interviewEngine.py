from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import json
from templates.prompts import question_gen_prompt, feedback_prompt
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

llm = ChatGroq(model="Gemma2-9b-It" , groq_api_key=groq_api_key)

question_chain = LLMChain(llm=llm, prompt=question_gen_prompt)
feedback_chain = LLMChain(llm=llm, prompt=feedback_prompt)

def generate_questions(subject):
    raw = question_chain.run({"subject": subject})
    try:
        return json.loads(raw)
    except Exception as e:
        print("Parsing error:", raw)
        return []

def evaluate_answer(question, ideal_answer, user_answer):
    return feedback_chain.run({
        "question": question,
        "ideal_answer": ideal_answer,
        "user_answer": user_answer
    })
