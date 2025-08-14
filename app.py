import random
import re
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

unaskable = ['the','be' ,'is', 'are', 'was', 'were', 'am', 'of', 'at', 'in', 'on', 
             'to', 'by', 'and', 'but', 'if', 'then', 'with', 'as', 'for', 
             'from', 'a', 'an', 'he', 'she', 'it', 'its','you', 'they', 'we', 'this',
             'that', 'these', 'those', 'because', 'although', 'unless', 'while',
             'during', 'since', 'do', 'does', 'did', 'done', 'or', 'always',
             'usually', 'sometimes', 'never', 'often', 'frequently', 'sometimes',
             'occasionally', 'rarely', 'seldom', 'me', 'him', 'them', 'us', 'her',
             'mine', 'my', 'your', 'yours', 'his', 'her', 'hers', 'our', 'ours', 
             'their', 'theirs', 'mainly', 'has', 'have', 'had','around', 'total', 'main']

@app.route('/notes', methods=["POST"])
def recieving():
    global generated_questions, generated_answers, unaskable, timer
    data = request.get_json()
    notes = data.get('notes')
    timer = data.get('timer')
    notes = re.split(r'(?<!\d)\.(?!\d)', notes)
    
    if notes[-1] == "":
        notes = notes[:-1]
    number_of_questions = int(data.get('number'))

    if number_of_questions > len(notes):
        return jsonify({'message':f'Maximum number of questions based on your notes is {len(notes)}'})
    else:
        sentences = random.sample(notes, number_of_questions)
    generated_questions = []
    generated_answers = []
    for sentence in sentences:
        words = sentence.split(" ")
        answer_unreplaced = random.choice(words)
        answer = answer_unreplaced.replace(".", "").replace(",", "").replace(";", "").replace(":", "")
        answer = answer.replace("-", "").replace("!","").replace("?", "").replace(";", "").lower()
        while (answer in unaskable) or (len(answer) < 2) or ('(' in answer) or (')' in answer):
            answer_unreplaced = random.choice(words)
            answer = answer_unreplaced.replace(".", "").replace(",", "").replace(";", "").replace(":", "")
            answer = answer.replace("-", "").replace("!","").replace("?", "").replace(";", "").lower()
        dots = '.' * len(answer)
        words[words.index(answer_unreplaced)] = dots

        question = ""
        for i in words:
            if question == "":
                question += i
            else:
                question += " " + i
    
        generated_questions.append(question)
        generated_answers.append(answer)
    print(generated_answers)
    return jsonify({'message': None})

@app.route('/quiz')
def quiz():
    global generated_questions, generated_answers, timer
    range_ = range(len(generated_questions))
    data = {
        'range_': range_,
        'generated_questions': generated_questions,
        'generated_answers': generated_answers,
        'timer': timer
    }
    return render_template('quiz.html', **data)

app.run(debug=True)