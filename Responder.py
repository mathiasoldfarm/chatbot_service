import json
import random

class Responder:
  def __init__(self):
    self.NO_TYPE = 0
    self.FETCH_NEXT_SESSION = 1 #"FETCH_NEXT_SESSION"
    self.FETCH_NEXT_SESSION_AND_LEVEL_UP = "FETCH_NEXT_SESSION_AND_LEVEL_UP"
    self.FETCH_NEXT_SESSION_AND_LEVEL_DOWN = "FETCH_NEXT_SESSION_AND_LEVEL_DOWN"
    self.FETCH_PREVIOUS_SESSION = 2#"FETCH_PREVIOUS_SESSION"
    self.FETCH_SESSION_BY_ID = 3
    self.SEARCH_FOR_CONTENT = 4
    self.FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN = "FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN"
    self.FETCH_NEXT_LEVEL = "FETCH_NEXT_LEVEL"
    self.FETCH_PREVIOUS_LEVEL = "FETCH_PREVIOUS_LEVEL"

    self.UNDERSTAND = "Jeg forstår"
    self.NOT_UNDERSTAND = "Jeg forstår ikke"
    self.NO_IDEA = "I have no idea"
    self.OH_DAMN = "Oh.. damn"
    self.SURE_LETS_GO = "Helt sikkert, lad os dykke ned i det!"

    self.answers_to_pick_from_init = [
      "Super godt, vi fortsætter",
      "Godt at høre, vi går videre",
      "Perfekt, her kommer næste afsnit"
    ]
    self.chosen_get_continue_answer = []

  def get_answer(self, question, context, history, _type, contextId):
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
      request_type = self.FETCH_NEXT_SESSION
      next_possible_questions = [self.SURE_LETS_GO]
      history_id = "NEW"
      SetDone = False
    elif question == self.UNDERSTAND or question == self.SURE_LETS_GO:
      if question == self.SURE_LETS_GO:
        answer = 'Godt, start med at læse dette'
      else:
        answer = self.get_continue_answer()
      request_type = self.FETCH_NEXT_SESSION
      next_possible_questions = [self.UNDERSTAND, self.NOT_UNDERSTAND]
    elif question == self.NOT_UNDERSTAND:
      answer = "No problem, I will try to find a better way of explaining."
      request_type = self.FETCH_PREVIOUS_SESSION
      next_possible_questions = [self.UNDERSTAND, self.NOT_UNDERSTAND]
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
        next_possible_questions = [self.UNDERSTAND, self.NOT_UNDERSTAND]
        request_type = self.FETCH_PREVIOUS_SESSION #FETCH_PREVIOUS_SESSION_AND_LEVEL_DOWN
        SetDone = False
      elif number_of_corrects == len(question_ids):
        answer = "Tillykke! Alle dine svar var rigtige. Vi fortsætter."
        next_possible_questions = [self.UNDERSTAND, self.NOT_UNDERSTAND]
        request_type = self.FETCH_NEXT_SESSION
      else:
        answer = "Ikke alle dine svar var rigtige, men vi får styr på det."
        next_possible_questions = [self.UNDERSTAND, self.NOT_UNDERSTAND]
        request_type = self.FETCH_PREVIOUS_SESSION
        SetDone = False
    elif _type == "section":
      answer = "Den får du her:"
      request_type = self.FETCH_SESSION_BY_ID
      next_possible_questions = [self.UNDERSTAND, self.NOT_UNDERSTAND]
    elif _type == "search":
      answer = "This is what I found:|I couldn't find any results. Try adjusting your search."
      request_type = self.SEARCH_FOR_CONTENT
      next_possible_questions = [self.UNDERSTAND, self.NOT_UNDERSTAND]
    else:
      answer = "Couldn't process question"
      next_possible_questions = [self.OH_DAMN]
      request_type = self.NO_TYPE
    return {
      "Answer": answer,
      "Type": request_type,
      "NextPossibleAnswers": next_possible_questions,
      "NextContextId": int(contextId) + 1,
      "GetNewHistory": history_id == "NEW",
      "SetDone": SetDone
    }

  def get_continue_answer(self):
    if len(self.chosen_get_continue_answer) == len(self.answers_to_pick_from_init):
      self.chosen_get_continue_answer = []
      answers_to_pick_from = self.answers_to_pick_from_init
    else:
      answers_to_pick_from = list(filter(lambda x: x not in self.chosen_get_continue_answer, self.answers_to_pick_from_init))

    chosen = random.choice(answers_to_pick_from)
    self.chosen_get_continue_answer.append(chosen)

    return chosen

    

