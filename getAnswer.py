import json

FETCH_NEXT_SESSION = "FETCH_NEXT_SESSION"
FETCH_NEXT_SESSION_AND_LEVEL_UP = "FETCH_NEXT_SESSION_AND_LEVEL_UP"
FETCH_NEXT_SESSION_AND_LEVEL_DOWN = "FETCH_NEXT_SESSION_AND_LEVEL_DOWN"
FETCH_PREVIOUS_SESSION = "FETCH_PREVIOUS_SESSION"
FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN = "FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN"
FETCH_NEXT_LEVEL = "FETCH_NEXT_LEVEL"
FETCH_PREVIOUS_LEVEL = "FETCH_PREVIOUS_LEVEL"

UNDERSTAND = "I understand this"
NOT_UNDERSTAND = "I do not understand this"
NO_IDEA = "I have no idea"
OH_DAMN = "Oh.. damn"

def getAnswer(question, context):
  context = json.loads(context)
  try:
    question = json.loads(question)
  except:
    pass
  answer = ""
  request_type = ""
  context_id = None
  session_group = None
  next_possible_questions = []
  if question == "BEGINNING":
    answer = "Hi Mathias, I will help you today with fractions"
    next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
    session_group = "NEW"
  elif question == UNDERSTAND:
    answer = "Perfect let's move on"
    request_type = FETCH_NEXT_SESSION
    next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
  elif question == NOT_UNDERSTAND:
    answer = "No problem, I will try to find a better way of explaining."
    request_type = FETCH_PREVIOUS_LEVEL
    next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
  elif isinstance(question, dict):
    if "question" in question:
      correct = context[0]["correct"]
      if int(correct) == int(question["question"]):
        answer = "Congratulations, your answer is correct. We'll continue"
        next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
        request_type = FETCH_NEXT_SESSION
      else:
        answer = "Your answer wasn't correct. We'll try to explain the subject again"
        next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
        request_type = FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN
  else:
    answer = "Couldn't process question"
    next_possible_questions = [OH_DAMN]
  return {
    "answer": answer,
    "request_type": request_type,
    "next_possible_questions": next_possible_questions,
    "context_id": context_id,
    "session_group": session_group
  }