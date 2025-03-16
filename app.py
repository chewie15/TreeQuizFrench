"""
Web version of the tree taxonomy quiz application
"""
from flask import Flask, render_template, request, jsonify, session
import random
import unicodedata
import string
from tree_data import TREES, HELP_TEXT, DIFFICULTY_LEVELS

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management

# Store session data
quiz_data = {
    'correct_answers': 0,
    'total_questions': 0,
    'current_tree': None,
    'current_type': '',
    'current_answer': '',
    'difficulty': 'facile',  # Default difficulty
    'attempts': 0  # Track number of attempts for current question
}

def normalize_answer(text):
    """Normalize text for comparison:
    - Remove accents
    - Convert to lowercase
    - Remove punctuation
    - Remove extra spaces
    - Handle singular/plural
    """
    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove accents
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                  if unicodedata.category(c) != 'Mn')

    # Remove punctuation
    text = ''.join(c for c in text if c not in string.punctuation)

    # Remove extra spaces
    text = ' '.join(text.split())

    # Handle singular/plural by removing trailing 's'
    text = text.rstrip('s')

    return text

def get_genus_species_count():
    """Count how many species exist for each genus"""
    genus_count = {}
    for _, genus, _, _ in TREES:
        genus_count[genus] = genus_count.get(genus, 0) + 1
    return genus_count

@app.route('/')
def home():
    """Render the quiz page"""
    return render_template('quiz.html', difficulties=DIFFICULTY_LEVELS.keys())

@app.route('/set-difficulty', methods=['POST'])
def set_difficulty():
    """Set the quiz difficulty level"""
    difficulty = request.json.get('difficulty', 'facile')
    if difficulty in DIFFICULTY_LEVELS:
        quiz_data['difficulty'] = difficulty
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Invalid difficulty level'}), 400

@app.route('/new-question')
def new_question():
    """Generate a new question based on current difficulty"""
    # Reset attempts counter for new question
    quiz_data['attempts'] = 0

    # Select a random tree
    quiz_data['current_tree'] = random.choice(TREES)
    name, genus, species = quiz_data['current_tree'][:3]  # Ignore image path for now

    # Check if this genus has multiple species
    genus_count = get_genus_species_count()
    has_multiple_species = genus_count[genus] > 1

    # All possible questions
    all_options = [
        ("nom français", "nom", name),
        ("genre (en latin)", "genre", genus) if not has_multiple_species else None,
        ("espèce (en latin)", "espèce", species)
    ]
    # Remove None values (when genre is excluded due to multiple species)
    all_options = [opt for opt in all_options if opt is not None]

    # Number of elements to guess based on difficulty
    num_questions = min(DIFFICULTY_LEVELS[quiz_data['difficulty']], len(all_options))

    # Randomly select which elements to ask
    selected_options = random.sample(all_options, num_questions)
    questions = []
    hints = []

    # Process each option as either a question or a hint
    for opt in all_options:
        if opt in selected_options:
            # Use "l'" instead of "le" for "espèce"
            question_text = f"l'{opt[0]}" if opt[0].startswith('e') else f"le {opt[0]}"
            questions.append(question_text)
            quiz_data[f'answer_{opt[1]}'] = opt[2]  # Store answer
        else:
            # Skip adding genre as hint if there are multiple species for this genus
            if has_multiple_species and opt[1] == 'genre':
                continue
            hints.append(f"🌳 {opt[0]}: {opt[2]}")

    # Join questions with proper French conjunction
    if len(questions) > 1:
        questions[-1] = "et " + questions[-1]
    question_text = ", ".join(questions)

    quiz_data['expected_answers'] = [opt[1] for opt in selected_options]

    return jsonify({
        'question': f"Pour cet arbre, trouvez {question_text} :",
        'hints': hints,
        'num_answers': num_questions,
        'attempts': quiz_data['attempts']
    })

@app.route('/check-answer', methods=['POST'])
def check_answer():
    """Check the submitted answers"""
    answers = request.json.get('answers', {})

    if not answers:
        return jsonify({
            'error': 'Veuillez entrer une réponse avant de valider.'
        }), 400

    # Increment attempts counter
    quiz_data['attempts'] += 1
    show_answers = quiz_data['attempts'] >= 3  # Show answers after 3 attempts

    correct_count = 0
    results = {}

    # Check each expected answer
    for answer_type in quiz_data['expected_answers']:
        user_answer = normalize_answer(answers.get(answer_type, ''))
        correct_answer = normalize_answer(quiz_data[f'answer_{answer_type}'])

        is_correct = user_answer == correct_answer
        if is_correct:
            correct_count += 1

        results[answer_type] = {
            'is_correct': is_correct,
            'correct_answer': quiz_data[f'answer_{answer_type}'],
            'show_answer': show_answers  # Add flag to show answer after 3 attempts
        }

    # Only count as a completed question if either all answers are correct or we've used all attempts
    if correct_count == len(quiz_data['expected_answers']) or show_answers:
        quiz_data['total_questions'] += 1
        if correct_count == len(quiz_data['expected_answers']):
            quiz_data['correct_answers'] += 1

    percentage = int(quiz_data['correct_answers'] / quiz_data['total_questions'] * 100) if quiz_data['total_questions'] > 0 else 0

    return jsonify({
        'results': results,
        'all_correct': correct_count == len(quiz_data['expected_answers']),
        'attempts_left': 3 - quiz_data['attempts'],
        'show_answers': show_answers,
        'score': f"Score: {quiz_data['correct_answers']}/{quiz_data['total_questions']} ({percentage}%)"
    })

@app.route('/help')
def help():
    """Get help text"""
    return jsonify({'help_text': HELP_TEXT})

if __name__ == '__main__':
    # ALWAYS serve the app on port 5000
    app.run(host='0.0.0.0', port=5000)