"""
Main application file for the tree taxonomy quiz
"""

import tkinter as tk
import random
from tkinter import messagebox
from quiz_ui import QuizUI
from tree_data import TREES, HELP_TEXT

class TreeQuiz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz des Arbres")
        self.root.geometry("500x800")  # Increased height for image

        self.ui = QuizUI(self.root)
        self.setup_handlers()

        self.correct_answers = 0
        self.total_questions = 0
        self.current_answer = ""
        self.current_tree = None
        self.current_type = ""

        self.new_question()

    def setup_handlers(self):
        """Setup event handlers"""
        self.ui.check_button.configure(command=self.check_answer)
        self.ui.new_question_button.configure(command=self.new_question)
        self.ui.help_button.configure(command=self.show_help)
        self.ui.entry.bind('<Return>', lambda e: self.check_answer())

    def new_question(self):
        """Generate and display a new question"""
        # Select a random tree
        self.current_tree = random.choice(TREES)
        name, genus, species, image_path = self.current_tree

        # Update the image
        self.ui.set_image(image_path)

        # Choose what to ask (nom, genre, or espèce)
        options = [
            ("nom français", "nom", name),
            ("genre (en latin)", "genre", genus),
            ("espèce (en latin)", "espèce", species)
        ]
        question_text, self.current_type, self.current_answer = random.choice(options)

        # Update question text
        self.ui.question_label.configure(
            text=f"Pour cet arbre, quel est son {question_text} ?"
        )

        # Show known information as hints
        hints = []
        if self.current_type != "nom":
            hints.append(f"🌳 Nom français: {name}")
        if self.current_type != "genre":
            hints.append(f"🧬 Genre (latin): {genus}")
        if self.current_type != "espèce":
            hints.append(f"🔍 Espèce (latin): {species}")

        self.ui.hint_label.configure(
            text="\n".join(hints)
        )

        # Clear previous answer and result
        self.ui.entry.delete(0, tk.END)
        self.ui.result_label.configure(text="")

    def check_answer(self):
        """Validate user's answer"""
        user_input = self.ui.entry.get().strip().lower()

        if not user_input:
            messagebox.showwarning(
                "Réponse vide",
                "Veuillez entrer une réponse avant de valider."
            )
            return

        self.total_questions += 1

        if user_input == self.current_answer.lower():
            self.correct_answers += 1
            self.ui.result_label.configure(
                text="✨ Bonne réponse ! ✨",
                foreground="green"
            )
        else:
            self.ui.result_label.configure(
                text=f"❌ Incorrect. La réponse était : {self.current_answer}",
                foreground="red"
            )

        # Update score
        percentage = int(self.correct_answers/self.total_questions*100)
        self.ui.score_label.configure(
            text=f"Score: {self.correct_answers}/{self.total_questions} ({percentage}%)"
        )

    def show_help(self):
        """Display help information"""
        messagebox.showinfo("Aide", HELP_TEXT)

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    quiz = TreeQuiz()
    quiz.run()