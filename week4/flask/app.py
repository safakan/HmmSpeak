from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# Sample trivia questions
TRIVIA_QUESTIONS = [
    {
        'question': 'What is the capital of France?',
        'options': ['London', 'Berlin', 'Paris', 'Madrid'],
        'correct_answer': 'Paris'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
        'correct_answer': 'Mars'
    },
    {
        'question': 'What is the largest mammal in the world?',
        'options': ['African Elephant', 'Blue Whale', 'Giraffe', 'Hippopotamus'],
        'correct_answer': 'Blue Whale'
    }
]

@app.route('/')
def index():
    # Initialize or reset the session
    if 'current_question' not in session:
        session['current_question'] = 0
        session['score'] = 0
    
    # Get the current question
    question_index = session['current_question']
    if question_index >= len(TRIVIA_QUESTIONS):
        return render_template('results.html', score=session['score'], total=len(TRIVIA_QUESTIONS))
    
    question = TRIVIA_QUESTIONS[question_index]
    return render_template('question.html', question=question)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    question_index = session['current_question']
    selected_answer = request.form.get('answer')
    correct_answer = TRIVIA_QUESTIONS[question_index]['correct_answer']
    
    if selected_answer == correct_answer:
        session['score'] = session.get('score', 0) + 1
    
    session['current_question'] = question_index + 1
    return redirect(url_for('index'))

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
