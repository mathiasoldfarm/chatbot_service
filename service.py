import flask
from flask import request
from flask import make_response
from getAnswer import getAnswer

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<p>Welcome to the Chatbot API</p>"

@app.route('/getanswer', methods=['GET'])
def get_answer():
  question = request.args.get("question")
  context = request.args.get("context")
  history = request.args.get("history")
  request_type = request.args.get("type")
  context_id = request.args.get("contextId")
  answer = getAnswer(question, context, history, request_type, context_id)
  response = make_response(answer, 200)
  return response



app.run()