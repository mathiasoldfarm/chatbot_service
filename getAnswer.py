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
      corrects = []
      context_keys = list(context.keys())
      answered_keys = list(question["question"].keys())

      assert(len(context_keys) == len(answered_keys))

      for context_key, answer_key in zip(context_keys, answered_keys):
        context_val = context[context_key]
        answer_val = question["question"][answer_key]
        if int(context_val) == int(answer_val):
          corrects.append(int(answer_val))

      number_of_corrects = len(corrects)

      if number_of_corrects == 0:
        answer = "Your answers weren't correct. But don't worry, we'll figure it out!"
        next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
        request_type = FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN
      elif number_of_corrects == len(context_keys):
        answer = "Congratulations! You got all the answers correct. We'll continue."
        next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
        request_type = FETCH_NEXT_SESSION
      else:
        answer = "Not all of your answers were correct. Try to read this again and then try again"
        next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
        request_type = FETCH_PREVIOUS_SESSION
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