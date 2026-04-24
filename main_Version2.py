"""
MAIN - Entry point and game loop
Initializes pygame, manages game states, and runs the main loop
"""

import pygame
import sys
from constants import *
from game_logic import QuizGame
from menus import (MainMenu, ModeSelectionMenu, QuestionCountMenu, 
                   PauseMenu, ResultsScreen)
from ui_components import AnswerButton

class GameEngine:
    """
    Main game engine managing all states and transitions
    Handles rendering, input, and game flow
    """
    
    def __init__(self):
        """Initialize game engine and pygame"""
        # Initialize pygame
        pygame.init()
        
        # Create display window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Russian History Quiz - Pixel Art Edition")
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        
        # Fonts with pixel art aesthetic
        self.font_huge = pygame.font.Font(None, FONT_SIZE_HUGE)
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.font_tiny = pygame.font.Font(None, FONT_SIZE_TINY)
        
        # Game state
        self.current_state = GameState.MAIN_MENU
        self.running = True
        
        # Initialize menus
        self.main_menu = MainMenu()
        self.mode_menu = None
        self.question_count_menu = None
        self.pause_menu = None
        self.results_screen = None
        
        # Game instance
        self.quiz = None
        self.selected_game_mode = None
        self.answer_buttons = []
    
    def handle_events(self):
        """
        Handle all pygame events (keyboard, mouse, quit)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Pause menu hotkey
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.current_state == GameState.PLAYING:
                    self.current_state = GameState.PAUSED
                    self.pause_menu = PauseMenu()
            
            # State-specific input handling
            elif self.current_state == GameState.MAIN_MENU:
                self._handle_main_menu_input()
            elif self.current_state == GameState.MODE_SELECTION:
                self._handle_mode_selection_input()
            elif self.current_state == GameState.QUESTION_COUNT:
                if event.type == pygame.KEYDOWN:
                    self.question_count_menu.handle_event(event)
                self._handle_question_count_input()
            elif self.current_state == GameState.PLAYING:
                self._handle_playing_input()
            elif self.current_state == GameState.PAUSED:
                self._handle_pause_input()
            elif self.current_state == GameState.RESULTS:
                self._handle_results_input()
    
    def _handle_main_menu_input(self):
        """Handle main menu mouse clicks"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        self.main_menu.update(mouse_pos, mouse_pressed)
        
        if mouse_pressed:
            action = self.main_menu.handle_click(mouse_pos)
            if action == "play":
                self.current_state = GameState.MODE_SELECTION
                self.mode_menu = ModeSelectionMenu()
            elif action == "quit":
                self.running = False
    
    def _handle_mode_selection_input(self):
        """Handle game mode selection"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        self.mode_menu.update(mouse_pos, mouse_pressed)
        
        if mouse_pressed:
            action = self.mode_menu.handle_click(mouse_pos)
            if action == "classic":
                self.selected_game_mode = GameMode.CLASSIC
                self.current_state = GameState.QUESTION_COUNT
                self.question_count_menu = QuestionCountMenu(GameMode.CLASSIC)
            elif action == "sudden":
                self.selected_game_mode = GameMode.SUDDEN_DEATH
                self.start_quiz(DEFAULT_QUESTION_COUNT)
            elif action == "marathon":
                self.selected_game_mode = GameMode.MARATHON
                self.start_quiz(MAX_QUESTION_COUNT)
            elif action == "back":
                self.current_state = GameState.MAIN_MENU
    
    def _handle_question_count_input(self):
        """Handle question count selection"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        self.question_count_menu.update(mouse_pos, mouse_pressed)
        
        if mouse_pressed:
            action = self.question_count_menu.handle_click(mouse_pos)
            if action == "back":
                self.current_state = GameState.MODE_SELECTION
            elif isinstance(action, int):
                self.start_quiz(action)
    
    def _handle_playing_input(self):
        """Handle in-game input during quiz"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        # Update answer buttons
        for btn in self.answer_buttons:
            btn.update(mouse_pos, mouse_pressed)
        
        # Check for answer selection
        if mouse_pressed and not self.quiz.question_answered:
            for i, btn in enumerate(self.answer_buttons):
                if btn.is_clicked(mouse_pos, True):
                    is_correct = self.quiz.answer_question(i)
                    
                    # Update button states to show correct/incorrect
                    for j, answer_btn in enumerate(self.answer_buttons):
                        if j == i:
                            answer_btn.set_state("evaluated")
                        elif answer_btn.is_correct:
                            answer_btn.set_state("evaluated")
        
        # Check for next question button click
        elif mouse_pressed and self.quiz.question_answered:
            # Simple check: if mouse in right area and game not over
            if not self.quiz.game_over:
                # Could add a "next" button, for now just auto-advance
                pass
    
    def _handle_pause_input(self):
        """Handle pause menu input"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        self.pause_menu.update(mouse_pos, mouse_pressed)
        
        if mouse_pressed:
            action = self.pause_menu.handle_click(mouse_pos)
            if action == "resume":
                self.current_state = GameState.PLAYING
                self.pause_menu = None
            elif action == "quit":
                self.current_state = GameState.MAIN_MENU
                self.quiz = None
    
    def _handle_results_input(self):
        """Handle results screen input"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        self.results_screen.update(mouse_pos, mouse_pressed)
        
        if mouse_pressed:
            action = self.results_screen.handle_click(mouse_pos)
            if action == "restart":
                # Restart with same mode and question count
                self.start_quiz(
                    self.quiz.total_questions,
                    self.selected_game_mode
                )
            elif action == "menu":
                self.current_state = GameState.MAIN_MENU
                self.quiz = None
    
    def start_quiz(self, question_count, mode=None):
        """
        Start a new quiz game
        
        Args:
            question_count: int - Number of questions
            mode: str - Game mode (uses selected if not specified)
        """
        if mode is None:
            mode = self.selected_game_mode
        
        self.quiz = QuizGame(mode, question_count)
        self.current_state = GameState.PLAYING
        self._create_answer_buttons()
    
    def _create_answer_buttons(self):
        """Create answer buttons for current question"""
        self.answer_buttons = []
        
        button_width = ANSWER_BUTTON_WIDTH
        button_height = ANSWER_BUTTON_HEIGHT
        start_x = (SCREEN_WIDTH - button_width * 2 - ANSWER_BUTTON_GAP) // 2
        start_y = 300
        
        # Create 4 answer buttons in 2x2 grid
        for i, answer in enumerate(self.quiz.shuffled_answers):
            x = start_x + (i % 2) * (button_width + ANSWER_BUTTON_GAP)
            y = start_y + (i // 2) * (button_height + ANSWER_BUTTON_GAP)
            
            is_correct = (answer == self.quiz.current_correct_answer)
            btn = AnswerButton(x, y, button_width, button_height, answer, is_correct)
            self.answer_buttons.append(btn)
    
    def update(self):
        """
        Update game logic
        """
        # Check for quiz completion
        if self.current_state == GameState.PLAYING:
            if self.quiz.game_over:
                results = self.quiz.get_results_summary()
                self.results_screen = ResultsScreen(results)
                self.current_state = GameState.RESULTS
            elif self.quiz.question_answered:
                # Auto-advance to next question after delay
                import time
                time.sleep(2)
                self.quiz.next_question()
                self._create_answer_buttons()
    
    def draw(self):
        """
        Render current game state
        """
        if self.current_state == GameState.MAIN_MENU:
            self.main_menu.draw(self.screen, self.font_huge, self.font_large)
        
        elif self.current_state == GameState.MODE_SELECTION:
            self.mode_menu.draw(self.screen, self.font_huge, self.font_large, self.font_small)
        
        elif self.current_state == GameState.QUESTION_COUNT:
            self.question_count_menu.draw(self.screen, self.font_huge, self.font_large)
        
        elif self.current_state == GameState.PLAYING:
            self._draw_quiz()
            
            # Show pause hint
            hint = self.font_small.render("Press ESC to pause", True, COLOR_MEDIUM_GREY)
            self.screen.blit(hint, (SCREEN_WIDTH - 200, 10))
        
        elif self.current_state == GameState.PAUSED:
            # Draw game behind pause menu
            self._draw_quiz()
            self.pause_menu.draw(self.screen, self.font_huge, self.font_large)
        
        elif self.current_state == GameState.RESULTS:
            self.results_screen.draw(self.screen, self.font_huge, self.font_large, self.font_small)
        
        pygame.display.flip()
    
    def _draw_quiz(self):
        """
        Draw the quiz gameplay screen
        """
        self.screen.fill(COLOR_WHITE)
        
        # Draw header with progress
        header_text = f"Question {self.quiz.current_question_index}/{self.quiz.total_questions}"
        header = self.font_medium.render(header_text, True, COLOR_PURPLE)
        self.screen.blit(header, (30, 30))
        
        # Draw score
        score_text = f"Score: {self.quiz.score}/{self.quiz.current_question_index - 1}"
        score = self.font_medium.render(score_text, True, COLOR_GREEN)
        self.screen.blit(score, (SCREEN_WIDTH - 250, 30))
        
        # Draw timer
        time_remaining = int(self.quiz.get_question_time_remaining())
        timer_color = COLOR_RED if time_remaining < 10 else COLOR_BLACK
        timer_text = self.font_medium.render(f"Time: {time_remaining}s", True, timer_color)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 250, 70))
        
        # Draw progress bar
        progress_width = SCREEN_WIDTH - 60
        progress_height = 10
        progress_x = 30
        progress_y = 80
        
        progress_percentage = (self.quiz.current_question_index - 1) / self.quiz.total_questions
        
        pygame.draw.rect(self.screen, COLOR_LIGHT_GREY, 
                        (progress_x, progress_y, progress_width, progress_height))
        pygame.draw.rect(self.screen, COLOR_PURPLE,
                        (progress_x, progress_y, progress_width * progress_percentage, progress_height))
        pygame.draw.rect(self.screen, COLOR_BLACK,
                        (progress_x, progress_y, progress_width, progress_height), 2)
        
        # Draw question
        question_font = pygame.font.Font(None, 26)
        question_lines = self._wrap_text(self.quiz.current_question_text, question_font, SCREEN_WIDTH - 60)
        
        y_offset = 130
        for line in question_lines:
            text_surf = question_font.render(line, True, COLOR_BLACK)
            self.screen.blit(text_surf, (30, y_offset))
            y_offset += 35
        
        # Draw answer buttons
        for btn in self.answer_buttons:
            btn.draw(self.screen, self.font_small)
        
        # Draw next button if answered
        if self.quiz.question_answered:
            next_text = "Press SPACE for next" if self.quiz.current_question_index < self.quiz.total_questions else "Quiz Complete"
            next_label = self.font_small.render(next_text, True, COLOR_BLUE)
            self.screen.blit(next_label, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 40))
    
    def _wrap_text(self, text, font, max_width):
        """
        Wrap text to fit within max width
        
        Args:
            text: str - Text to wrap
            font: pygame.font.Font - Font for measuring
            max_width: int - Maximum width
            
        Returns:
            list - Wrapped text lines
        """
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            if font.size(line_text)[0] > max_width:
                current_line.pop()
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines if lines else [text]
    
    def run(self):
        """
        Main game loop
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game"""
    engine = GameEngine()
    engine.run()


if __name__ == "__main__":
    main()