import json

FETCH_NEXT_SESSION = 1 #"FETCH_NEXT_SESSION"
FETCH_NEXT_SESSION_AND_LEVEL_UP = "FETCH_NEXT_SESSION_AND_LEVEL_UP"
FETCH_NEXT_SESSION_AND_LEVEL_DOWN = "FETCH_NEXT_SESSION_AND_LEVEL_DOWN"
FETCH_PREVIOUS_SESSION = 2#"FETCH_PREVIOUS_SESSION"
FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN = "FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN"
FETCH_NEXT_LEVEL = "FETCH_NEXT_LEVEL"
FETCH_PREVIOUS_LEVEL = "FETCH_PREVIOUS_LEVEL"

UNDERSTAND = "I understand this"
NOT_UNDERSTAND = "I do not understand this"
NO_IDEA = "I have no idea"
OH_DAMN = "Oh.. damn"
SURE_LETS_GO = "Sure, Let's go!"

def getAnswer(question, context, history, _type, contextId):
  context = json.loads(context)
  history = json.loads(history)
  try:
    question = json.loads(question)
  except:
    pass
  print(history)
  answer = ""
  request_type = None
  history_id = None
  next_possible_questions = []
  if question == "BEGINNING":
    request_type = FETCH_NEXT_SESSION
    next_possible_questions = [SURE_LETS_GO]
    history_id = "NEW"
  elif question == UNDERSTAND or question == SURE_LETS_GO:
    if question == SURE_LETS_GO:
      answer = 'Good, start by reading this text:'
    else:
      answer = "Perfect let's move on"
    request_type = FETCH_NEXT_SESSION
    next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
  elif question == NOT_UNDERSTAND:
    answer = "No problem, I will try to find a better way of explaining."
    request_type = FETCH_PREVIOUS_SESSION
    next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
  elif _type == "question":
    corrects = []
    question_ids = list(context.keys())

    for question_id in question_ids:
      correct = context[question_id]
      answered = question[question_id]
      if correct == answered:
        corrects.append(question_id)

    number_of_corrects = len(corrects)

    if number_of_corrects == 0:
      answer = "Your answers weren't correct. But don't worry, we'll figure it out!"
      next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
      request_type = FETCH_PREVIOUS_SESSION #FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN
    elif number_of_corrects == len(question_ids):
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
    "Answer": answer,
    "Type": request_type,
    "NextPossibleAnswers": next_possible_questions,
    "NextContextId": int(contextId) + 1,
    "GetNewHistory": history_id == "NEW"
  }