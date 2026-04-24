"""
GAME LOGIC - Quiz game state and mechanics
Handles question management, scoring, timers, and game flow
"""

import random
import time
from constants import *
from questions import QUESTIONS_DATA

class QuizGame:
    """
    Main quiz game logic handler
    Manages current question, scoring, timer, and game flow
    
    Attributes:
        mode: str - Current game mode (CLASSIC, SUDDEN_DEATH, MARATHON)
        total_questions: int - Number of questions to attempt
        current_question_index: int - Index of current question
        score: int - Number of correct answers
        start_time: float - When the quiz started
        question_start_time: float - When current question started
        question_answered: bool - Whether current question is answered
        game_over: bool - Whether the game has ended
    """
    
    def __init__(self, mode, question_count):
        """
        Initialize a new quiz game
        
        Args:
            mode: str - Game mode (CLASSIC, SUDDEN_DEATH, MARATHON)
            question_count: int - Number of questions to ask
        """
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
        """
        Load the next question and generate shuffled answers
        Returns answer button data for UI to render
        """
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
        """
        Generate 3 incorrect answers and shuffle all 4
        
        Args:
            correct_answer: str - The correct answer text
            question_idx: int - Index of current question
            
        Returns:
            list - Shuffled answers with correct at index 0 before shuffle
        """
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
        """
        Process user's answer selection
        
        Args:
            answer_index: int - Index of selected answer (0-3)
            
        Returns:
            bool - True if answer is correct, False otherwise
        """
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
        """
        Move to next question in the quiz
        """
        if not self.game_over:
            self.load_question()
    
    def get_elapsed_time(self):
        """
        Get time elapsed since quiz started
        
        Returns:
            float - Seconds elapsed
        """
        return time.time() - self.start_time
    
    def get_question_time_remaining(self):
        """
        Get time remaining for current question
        
        Returns:
            float - Seconds remaining (0 if time expired)
        """
        elapsed = time.time() - self.question_start_time
        remaining = QUESTION_TIMER_SECONDS - elapsed
        return max(0, remaining)
    
    def is_time_expired(self):
        """
        Check if time for current question has expired
        
        Returns:
            bool - True if time is up
        """
        return self.get_question_time_remaining() <= 0
    
    def get_score_percentage(self):
        """
        Calculate current score as percentage
        
        Returns:
            float - Score percentage (0-100)
        """
        if self.current_question_index == 0:
            return 0
        return (self.score / self.current_question_index) * 100
    
    def get_results_summary(self):
        """
        Get final results and grade
        
        Returns:
            dict - Results data with score, percentage, and grade
        """
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