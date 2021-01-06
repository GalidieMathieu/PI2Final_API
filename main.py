from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from Question_Answering import Question_Answering
from Spelling_correction import SpellingCorrection
import json

app = Flask(__name__)
api = Api(app)


@app.route('/api/questions', methods=['GET', 'POST', 'DELETE', 'PUT'])
def question():
    print("\n#############################################")
    print("question answering")
    data = request.get_json()
    return jsonify(reponse=Question_Answering.getQuestion(data['txt']))


@app.route('/api/isCorrect', methods=['GET', 'POST', 'DELETE', 'PUT'])
def SpellingCorrect():
    print("\n #############################################")
    print("Spelling Corrrect")
    data = request.get_json()
    response = str(SpellingCorrection.get(data["correctWord"], data["userWord"]))
    print(response)
    return jsonify(reponse=response)


if __name__ == '__main__':
    print("#############################################")
    print("démarage de l'api")
    app.run(debug=True)
