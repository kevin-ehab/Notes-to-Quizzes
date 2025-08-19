import random
import re
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

unaskable = {
    # Articles & determiners
    'a','an','the','this','that','these','those','some','any','each','every',
    'all','both','few','many','much','most','other','several','such','no','nor',

    # Pronouns
    'i','me','my','mine','myself',
    'we','us','our','ours','ourselves',
    'you','your','yours','yourself','yourselves',
    'he','him','his','himself',
    'she','her','hers','herself',
    'it','its','itself',
    'they','them','their','theirs','themselves',

    # Auxiliaries & modals
    'am','is','are','was','were','be','been','being',
    'do','does','did','done',
    'have','has','had','having',
    'will','would','shall','should','can','could','may','might','must',

    # Conjunctions & prepositions
    'and','but','if','or','because','although','though','unless','while',
    'before','after','during','since','until','once','when','whenever',
    'where','wherever','whereas','as','than','then',
    'of','at','in','on','to','by','for','with','from','about','into',
    'over','under','between','among','against','around','through','within',
    'without','upon','toward','towards','off',

    # Question words
    'who','whom','whose','which','what','why','how','where',

    # Frequency & filler adverbs
    'always','usually','sometimes','never','often','frequently','occasionally',
    'rarely','seldom','generally','mainly','mostly','partly','slightly',

    # Miscellaneous unhelpful
    'yes','no','not','very','just','only','also','even','too',
    'own','same','such','another','either','neither',
    'total','main'
}

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