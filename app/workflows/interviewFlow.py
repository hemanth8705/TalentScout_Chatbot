from services.interviewEngine import generate_questions, evaluate_answer

def run_interview(subjects, user_responses):
    results = {}
    for subject in subjects:
        questions = generate_questions(subject)
        results[subject] = {
            "questions": questions,
            "answers": [],
            "feedback": []
        }
        for q in questions:
            user_answer = user_responses.get(subject, {}).get(q["question"], "")
            feedback = evaluate_answer(q["question"], q["ideal_answer"], user_answer)
            results[subject]["answers"].append(user_answer)
            results[subject]["feedback"].append(feedback)
    return results
