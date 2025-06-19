import os
from flask import Flask, render_template, request, session, redirect
from recommend import recommend_cards

app = Flask(__name__)
app.secret_key = "your-secret-key"

questions = [
    "What is your monthly income (in ₹)?",
    "Where do you spend the most? (Fuel, Travel, Groceries, Dining)",
    "What benefits do you prefer? (Cashback, Travel Points, Lounge Access)",
    "Do you have any existing credit cards? (Optional)",
    "What is your approximate credit score? (Poor, Average, Good, Unknown)"
]

fields = ["income", "spending", "benefits", "existing_cards", "credit_score"]

@app.route('/', methods=['GET', 'POST'])
def chat():
    # Initialize all session variables if not present
    if 'step' not in session:
        session['step'] = 0
    if 'answers' not in session:
        session['answers'] = {}
    if 'history' not in session:
        session['history'] = []

    step = session['step']
    answers = session['answers']
    history = session['history']

    if request.method == 'POST':
        user_input = request.form['message']
        field_key = fields[step]
        question = questions[step]

        # Save Q&A to session
        answers[field_key] = user_input
        history.append({"role": "assistant", "text": question})
        history.append({"role": "user", "text": user_input})

        # Update session state
        session['answers'] = answers
        session['history'] = history
        session['step'] = step + 1

        # All questions answered
        if session['step'] >= len(questions):
            return redirect('/summary')

    # Show next question
    next_question = questions[session['step']] if session['step'] < len(questions) else None
    return render_template('chat.html', response=next_question, history=session['history'])

@app.route('/summary', methods=['GET', 'POST'])
def summary():
    answers = session.get('answers', {})
    cards = recommend_cards(answers)
    return render_template('summary.html', answers=answers, cards=cards)

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
