from langchain.prompts import PromptTemplate

question_gen_prompt = PromptTemplate.from_template("""
You are an expert technical interviewer.
Generate 3 technical interview questions and their ideal answers for the subject: {subject}.
Return the output in strict JSON format:
[
  {{"question": "...", "ideal_answer": "..."}},
  ...
]
""")

feedback_prompt = PromptTemplate.from_template("""
You are a technical interviewer. Evaluate the candidate's answer.
Question: {question}
Ideal Answer: {ideal_answer}
Candidate's Answer: {user_answer}

Give a short and polite evaluation. Mention if it's correct/partial/incorrect. Suggest improvements if needed.
""")
