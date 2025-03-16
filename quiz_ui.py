"""
UI components and styling for the tree quiz application
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class QuizUI:
    def __init__(self, root):
        self.root = root
        self.setup_styles()
        self.create_widgets()
        self.current_image = None  # Keep reference to prevent garbage collection

    def setup_styles(self):
        """Configure styles for UI elements"""
        style = ttk.Style()
        style.configure('Title.TLabel', 
                       font=('Helvetica', 16, 'bold'),
                       padding=10)
        style.configure('Question.TLabel',
                       font=('Helvetica', 12, 'bold'),
                       padding=5,
                       wraplength=400)
        style.configure('Hint.TLabel',
                       font=('Helvetica', 11),
                       padding=5,
                       wraplength=400)
        style.configure('Result.TLabel',
                       font=('Helvetica', 12, 'bold'),
                       padding=5)
        style.configure('Score.TLabel',
                       font=('Helvetica', 10),
                       padding=5)

    def create_widgets(self):
        """Create and arrange UI widgets"""
        # Title
        self.title_label = ttk.Label(
            self.root,
            text="Quiz de Taxonomie des Arbres",
            style='Title.TLabel'
        )
        self.title_label.pack(pady=10)

        # Image frame
        self.image_frame = ttk.Frame(self.root)
        self.image_frame.pack(pady=10)

        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack()

        # Question
        self.question_frame = ttk.Frame(self.root)
        self.question_frame.pack(fill=tk.X, padx=20)

        self.question_label = ttk.Label(
            self.question_frame,
            text="",
            style='Question.TLabel'
        )
        self.question_label.pack(pady=10)

        # Hints
        self.hint_label = ttk.Label(
            self.question_frame,
            text="",
            style='Hint.TLabel',
            justify=tk.LEFT
        )
        self.hint_label.pack(pady=10)

        # Entry
        self.entry_frame = ttk.Frame(self.root)
        self.entry_frame.pack(fill=tk.X, padx=20, pady=10)

        self.entry = ttk.Entry(
            self.entry_frame,
            font=('Helvetica', 12)
        )
        self.entry.pack(fill=tk.X)

        # Buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.check_button = ttk.Button(
            self.button_frame,
            text="Valider"
        )
        self.check_button.pack(side=tk.LEFT, padx=5)

        self.new_question_button = ttk.Button(
            self.button_frame,
            text="Nouvelle question"
        )
        self.new_question_button.pack(side=tk.LEFT, padx=5)

        self.help_button = ttk.Button(
            self.button_frame,
            text="Aide"
        )
        self.help_button.pack(side=tk.LEFT, padx=5)

        # Result
        self.result_label = ttk.Label(
            self.root,
            text="",
            style='Result.TLabel'
        )
        self.result_label.pack(pady=10)

        # Score
        self.score_label = ttk.Label(
            self.root,
            text="Score: 0/0",
            style='Score.TLabel'
        )
        self.score_label.pack()

    def set_image(self, image_path):
        """Update the displayed image"""
        try:
            # Open and resize image
            image = Image.open(image_path)
            # Calculate new size while maintaining aspect ratio
            max_size = (300, 300)
            ratio = min(max_size[0]/image.width, max_size[1]/image.height)
            new_size = (int(image.width*ratio), int(image.height*ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)

            # Convert to PhotoImage and display
            self.current_image = ImageTk.PhotoImage(image)
            self.image_label.configure(image=self.current_image)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            self.image_label.configure(image="")