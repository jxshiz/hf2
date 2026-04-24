import random
import time
from constants import *
from questions import QUESTIONS_DATA

class QuizGame:
    # logic handler
    def __init__(self, mode, question_count):
        self.mode = mode
        self.total_questions = question_count if mode != GameMode.MARATHON else MAX_QUESTION_COUNT
        self.current_question_index = 0
        self.score = 0
        self.answered_questions = set()  # Track answered questions in marathon mode
        
        # Timing
        self.start_time = time.time()
        self.question_start_time = time.time()
        self.question_answered = False
        self.game_over = False
        
        # Shuffle questions and prepare first question
        self.question_indices = list(range(len(QUESTIONS_DATA)))
        random.shuffle(self.question_indices)
        
        # For marathon mode, we need all questions available
        if mode == GameMode.MARATHON:
            self.all_questions_used = set()
        
        self.load_question()
    
    def load_question(self):
        # Check if we've completed the quiz
        if self.mode == GameMode.MARATHON:
            # Marathon ends when all unique questions are answered correctly
            if len(self.all_questions_used) >= len(QUESTIONS_DATA):
                self.game_over = True
                return None
        else:
            if self.current_question_index >= self.total_questions:
                self.game_over = True
                return None
        
        # Get next question index
        if self.mode == GameMode.MARATHON:
            # Find next unanswered question
            for i in range(len(QUESTIONS_DATA)):
                if i not in self.all_questions_used:
                    question_idx = i
                    break
        else:
            question_idx = self.question_indices[self.current_question_index]
        
        # Get question data
        question_data = QUESTIONS_DATA[question_idx]
        self.current_question_text = question_data[0]
        self.current_correct_answer = question_data[1]
        self.current_question_idx = question_idx
        
        # Generate and shuffle answers
        self.shuffled_answers = self._generate_shuffled_answers(
            self.current_correct_answer, 
            question_idx
        )
        
        # Reset for new question
        self.question_answered = False
        self.question_start_time = time.time()
        self.current_question_index += 1
    
    def _generate_shuffled_answers(self, correct_answer, question_idx):
        # Get 3 incorrect answers from other questions
        wrong_answers = []
        available_indices = [i for i in range(len(QUESTIONS_DATA)) if i != question_idx]
        random.shuffle(available_indices)
        
        for idx in available_indices:
            if len(wrong_answers) >= 3:
                break
            if QUESTIONS_DATA[idx][1] != correct_answer:
                wrong_answers.append(QUESTIONS_DATA[idx][1])
        
        # Combine and shuffle
        all_answers = [correct_answer] + wrong_answers[:3]
        shuffled = all_answers.copy()
        random.shuffle(shuffled)
        
        return shuffled
    
    def answer_question(self, answer_index):
        if self.question_answered:
            return None
        
        self.question_answered = True
        selected_answer = self.shuffled_answers[answer_index]
        is_correct = selected_answer == self.current_correct_answer
        
        if is_correct:
            self.score += 1
            if self.mode == GameMode.MARATHON:
                self.all_questions_used.add(self.current_question_idx)
        else:
            # Sudden death mode: game over on first wrong answer
            if self.mode == GameMode.SUDDEN_DEATH:
                self.game_over = True
        
        return is_correct
    
    def next_question(self):
        if not self.game_over:
            self.load_question()
    
    def get_elapsed_time(self):
        return time.time() - self.start_time
    
    def get_question_time_remaining(self):
        elapsed = time.time() - self.question_start_time
        remaining = QUESTION_TIMER_SECONDS - elapsed
        return max(0, remaining)
    
    def is_time_expired(self):
        return self.get_question_time_remaining() <= 0
    
    def get_score_percentage(self):
        if self.current_question_index == 0:
            return 0
        return (self.score / self.current_question_index) * 100
    
    def get_results_summary(self):
        percentage = self.get_score_percentage()
        
        # Assign letter grade
        if percentage >= 90:
            grade = "A*"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 50:
            grade = "D"
        else:
            grade = "F"
        
        total_time = int(self.get_elapsed_time())
        
        return {
            "score": self.score,
            "total": self.current_question_index - 1 if not self.game_over else self.current_question_index,
            "percentage": percentage,
            "grade": grade,
            "time": total_time,
            "mode": self.mode
        }
