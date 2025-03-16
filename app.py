import streamlit as st
import random
import unicodedata
import string
from tree_data import TREES, HELP_TEXT, DIFFICULTY_LEVELS

# Store session data with Streamlit
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = {
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
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
    text = ''.join(c for c in text if c not in string.punctuation)
    text = ' '.join(text.split())
    text = text.rstrip('s')
    return text

def get_genus_species_count():
    """Count how many species exist for each genus"""
    genus_count = {}
    for _, genus, _, _ in TREES:
        genus_count[genus] = genus_count.get(genus, 0) + 1
    return genus_count

def new_question():
    """Generate a new question based on current difficulty"""
    st.session_state.quiz_data['attempts'] = 0
    st.session_state.quiz_data['current_tree'] = random.choice(TREES)
    name, genus, species = st.session_state.quiz_data['current_tree'][:3]
    genus_count = get_genus_species_count()
    has_multiple_species = genus_count[genus] > 1
    all_options = [
        ("nom français", "nom", name),
        ("genre (en latin)", "genre", genus) if not has_multiple_species else None,
        ("espèce (en latin)", "espèce", species)
    ]
    all_options = [opt for opt in all_options if opt is not None]
    num_questions = min(DIFFICULTY_LEVELS[st.session_state.quiz_data['difficulty']], len(all_options))
    selected_options = random.sample(all_options, num_questions)
    questions = []
    hints = []
    for opt in all_options:
        if opt in selected_options:
            question_text = f"l'{opt[0]}" if opt[0].startswith('e') else f"le {opt[0]}"
            questions.append(question_text)
            st.session_state.quiz_data[f'answer_{opt[1]}'] = opt[2]
        else:
            if has_multiple_species and opt[1] == 'genre':
                continue
            hints.append(f"🌳 {opt[0]}: {opt[2]}")
    if len(questions) > 1:
        questions[-1] = "et " + questions[-1]
    question_text = ", ".join(questions)
    st.session_state.quiz_data['expected_answers'] = [opt[1] for opt in selected_options]
    return f"Pour cet arbre, trouvez {question_text} :", hints

def check_answer(answers):
    if not answers:
        return {'error': 'Veuillez entrer une réponse avant de valider.'}, False
    st.session_state.quiz_data['attempts'] += 1
    show_answers = st.session_state.quiz_data['attempts'] >= 3
    correct_count = 0
    results = {}
    for answer_type in st.session_state.quiz_data['expected_answers']:
        user_answer = normalize_answer(answers.get(answer_type, ''))
        correct_answer = normalize_answer(st.session_state.quiz_data[f'answer_{answer_type}'])
        is_correct = user_answer == correct_answer
        if is_correct:
            correct_count += 1
        results[answer_type] = {
            'is_correct': is_correct,
            'correct_answer': st.session_state.quiz_data[f'answer_{answer_type}'],
            'show_answer': show_answers
        }
    if correct_count == len(st.session_state.quiz_data['expected_answers']) or show_answers:
        st.session_state.quiz_data['total_questions'] += 1
        if correct_count == len(st.session_state.quiz_data['expected_answers']):
            st.session_state.quiz_data['correct_answers'] += 1
    percentage = int(st.session_state.quiz_data['correct_answers'] / st.session_state.quiz_data['total_questions'] * 100) if st.session_state.quiz_data['total_questions'] > 0 else 0
    return {
        'results': results,
        'all_correct': correct_count == len(st.session_state.quiz_data['expected_answers']),
        'attempts_left': 3 - st.session_state.quiz_data['attempts'],
        'show_answers': show_answers,
        'score': f"Score: {st.session_state.quiz_data['correct_answers']}/{st.session_state.quiz_data['total_questions']} ({percentage}%)"
    }, True

# Streamlit app
st.title("Tree Taxonomy Quiz")
difficulty = st.selectbox("Select Difficulty", list(DIFFICULTY_LEVELS.keys()))
st.session_state.quiz_data['difficulty'] = difficulty

if st.button("New Question"):
    question, hints = new_question()
    st.session_state.question = question
    st.session_state.hints = hints

if 'question' in st.session_state:
    st.write(st.session_state.question)
    for hint in st.session_state.hints:
        st.write(hint)
    answers = {}
    for answer_type in st.session_state.quiz_data['expected_answers']:
        answers[answer_type] = st.text_input(f"Answer for {answer_type}")
    if st.button("Submit Answer"):
        results, success = check_answer(answers)
        if not success:
            st.write(results['error'])
        else:
            for answer_type, result in results['results'].items():
                st.write(f"{answer_type}: {'Correct' if result['is_correct'] else 'Incorrect'}")
                if result['show_answer']:
                    st.write(f"Correct answer: {result['correct_answer']}")
            st.write(f"Attempts left: {results['attempts_left']}")
            st.write(results['score'])
