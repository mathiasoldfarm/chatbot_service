import flask
from flask import request
from flask import make_response
from getAnswer import getAnswer

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<p>Welcome to the Chatbot API</p>"

@app.route('/getanswer/<string:question>/<string:context>/<string:history>', methods=['GET'])
def get_answer(question, context, history):
  answer = getAnswer(question, context, history)
  response = make_response(answer, 200)
  return response



app.run()