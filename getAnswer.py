import json

NO_TYPE = 0
FETCH_NEXT_SESSION = 1 #"FETCH_NEXT_SESSION"
FETCH_NEXT_SESSION_AND_LEVEL_UP = "FETCH_NEXT_SESSION_AND_LEVEL_UP"
FETCH_NEXT_SESSION_AND_LEVEL_DOWN = "FETCH_NEXT_SESSION_AND_LEVEL_DOWN"
FETCH_PREVIOUS_SESSION = 2#"FETCH_PREVIOUS_SESSION"
FETCH_SESSION_BY_ID = 3
SEARCH_FOR_CONTENT = 4
FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN = "FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN"
FETCH_NEXT_LEVEL = "FETCH_NEXT_LEVEL"
FETCH_PREVIOUS_LEVEL = "FETCH_PREVIOUS_LEVEL"

UNDERSTAND = "Jeg forstår"
NOT_UNDERSTAND = "Jeg forstår ikke"
NO_IDEA = "I have no idea"
OH_DAMN = "Oh.. damn"
SURE_LETS_GO = "Helt sikkert, lad os dykke ned i det!"

def getAnswer(question, context, history, _type, contextId):
  context = json.loads(context)
  history = json.loads(history)
  try:
    question = json.loads(question)
  except:
    pass
  answer = ""
  request_type = None
  history_id = None
  SetDone = True
  next_possible_questions = []
  if question == "BEGINNING":
    request_type = FETCH_NEXT_SESSION
    next_possible_questions = [SURE_LETS_GO]
    history_id = "NEW"
    SetDone = False
  elif question == UNDERSTAND or question == SURE_LETS_GO:
    if question == SURE_LETS_GO:
      answer = 'Godt, start med at læse dette'
    else:
      answer = "Super godt, vi fortsætter"
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
      answer = "Dine svar var ikke korrekte, men fortvivl ej. Vi finder ud af det!"
      next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
      request_type = FETCH_PREVIOUS_SESSION #FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN
      SetDone = False
    elif number_of_corrects == len(question_ids):
      answer = "Tillykke! Alle dine svar var rigtige. Vi fortsætter."
      next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
      request_type = FETCH_NEXT_SESSION
    else:
      answer = "Ikke alle dine svar var rigtige, men vi får styr på det."
      next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
      request_type = FETCH_PREVIOUS_SESSION
      SetDone = False
  elif _type == "section":
    answer = "Den får du her:"
    request_type = FETCH_SESSION_BY_ID
    next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
  elif _type == "search":
    answer = "This is what I found:|I couldn't find any results. Try adjusting your search."
    request_type = SEARCH_FOR_CONTENT
    next_possible_questions = [UNDERSTAND, NOT_UNDERSTAND]
  else:
    answer = "Couldn't process question"
    next_possible_questions = [OH_DAMN]
    request_type = NO_TYPE
  return {
    "Answer": answer,
    "Type": request_type,
    "NextPossibleAnswers": next_possible_questions,
    "NextContextId": int(contextId) + 1,
    "GetNewHistory": history_id == "NEW",
    "SetDone": SetDone
  }