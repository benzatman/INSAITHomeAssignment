# app/main.py
from flask import Flask, request, jsonify
import openai
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)


class QnA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'Question is required'}), 400

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=150
    )

    answer = response.choices[0].text.strip()

    qna = QnA(question=question, answer=answer)
    db.session.add(qna)
    db.session.commit()

    return jsonify({'question': question, 'answer': answer})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
