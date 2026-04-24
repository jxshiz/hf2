"""
MENUS - Main menu, mode selection, pause menu, and results screen
Handles all menu UI and navigation between game states
"""

import pygame
from constants import *
from ui_components import Button, NumberInput

class MainMenu:
    """
    Main menu screen with pixel art aesthetic
    Options: Play, Settings, Quit
    """
    
    def __init__(self):
        """Initialize main menu"""
        self.buttons = []
        self._create_buttons()
    
    def _create_buttons(self):
        """Create menu buttons with pixel art spacing"""
        button_width = 200
        button_height = 60
        center_x = (SCREEN_WIDTH - button_width) // 2
        
        # Play button
        play_btn = Button(
            center_x,
            200,
            button_width,
            button_height,
            "PLAY",
            base_color=COLOR_GREEN,
            hover_color=COLOR_LIGHT_GREEN,
            click_color=COLOR_DARK_GREEN
        )
        self.buttons.append(("play", play_btn))
        
        # Settings button
        settings_btn = Button(
            center_x,
            300,
            button_width,
            button_height,
            "SETTINGS",
            base_color=COLOR_BLUE,
            hover_color=COLOR_CYAN,
            click_color=COLOR_PURPLE
        )
        self.buttons.append(("settings", settings_btn))
        
        # Quit button
        quit_btn = Button(
            center_x,
            400,
            button_width,
            button_height,
            "QUIT",
            base_color=COLOR_RED,
            hover_color=COLOR_LIGHT_RED,
            click_color=COLOR_DARK_RED
        )
        self.buttons.append(("quit", quit_btn))
    
    def update(self, mouse_pos, mouse_clicked):
        """
        Update menu button states
        
        Args:
            mouse_pos: tuple - Current mouse position
            mouse_clicked: bool - Whether mouse is clicked
        """
        for _, btn in self.buttons:
            btn.update(mouse_pos, mouse_clicked)
    
    def handle_click(self, mouse_pos):
        """
        Handle mouse click on menu
        
        Args:
            mouse_pos: tuple - Click position
            
        Returns:
            str - Action name or None
        """
        for action, btn in self.buttons:
            if btn.is_clicked(mouse_pos, True):
                return action
        return None
    
    def draw(self, surface, font_large, font_medium):
        """
        Draw main menu with title and buttons
        
        Args:
            surface: pygame.Surface - Surface to draw on
            font_large: pygame.font.Font - Large font for title
            font_medium: pygame.font.Font - Medium font for buttons
        """
        surface.fill(COLOR_WHITE)
        
        # Draw title with pixel art style
        title = font_large.render("RUSSIAN HISTORY", True, COLOR_PURPLE)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=50)
        surface.blit(title, title_rect)
        
        # Subtitle
        subtitle = font_large.render("QUIZ", True, COLOR_DARK_PURPLE)
        subtitle_rect = subtitle.get_rect(centerx=SCREEN_WIDTH // 2, y=110)
        surface.blit(subtitle, subtitle_rect)
        
        # Draw decorative line
        pygame.draw.line(surface, COLOR_PURPLE, 
                        (50, 160), (SCREEN_WIDTH - 50, 160), 5)
        
        # Draw all buttons
        for _, btn in self.buttons:
            btn.draw(surface, font_medium)


class ModeSelectionMenu:
    """
    Game mode selection menu
    Choose between Classic, Sudden Death, and Marathon modes
    """
    
    def __init__(self):
        """Initialize mode selection menu"""
        self.buttons = []
        self._create_buttons()
    
    def _create_buttons(self):
        """Create mode selection buttons"""
        button_width = 250
        button_height = 60
        center_x = (SCREEN_WIDTH - button_width) // 2
        
        # Classic mode
        classic_btn = Button(
            center_x, 150, button_width, button_height,
            "CLASSIC MODE",
            base_color=COLOR_BLUE,
            hover_color=COLOR_CYAN,
            click_color=COLOR_DARK_PURPLE
        )
        self.buttons.append(("classic", classic_btn, "Answer all questions. Standard mode."))
        
        # Sudden Death mode
        sudden_btn = Button(
            center_x, 270, button_width, button_height,
            "SUDDEN DEATH",
            base_color=COLOR_RED,
            hover_color=COLOR_LIGHT_RED,
            click_color=COLOR_DARK_RED
        )
        self.buttons.append(("sudden", sudden_btn, "One wrong answer = Game Over!"))
        
        # Marathon mode
        marathon_btn = Button(
            center_x, 390, button_width, button_height,
            "MARATHON",
            base_color=COLOR_GREEN,
            hover_color=COLOR_LIGHT_GREEN,
            click_color=COLOR_DARK_GREEN
        )
        self.buttons.append(("marathon", marathon_btn, "Answer all 1000 questions perfectly."))
        
        # Back button
        back_btn = Button(
            30, SCREEN_HEIGHT - 70, 100, 50,
            "BACK",
            base_color=COLOR_LIGHT_GREY,
            hover_color=COLOR_MEDIUM_GREY,
            click_color=COLOR_DARK_GREY
        )
        self.buttons.append(("back", back_btn, ""))
    
    def update(self, mouse_pos, mouse_clicked):
        """Update button states"""
        for _, btn, _ in self.buttons:
            btn.update(mouse_pos, mouse_clicked)
    
    def handle_click(self, mouse_pos):
        """
        Handle click on mode selection
        
        Returns:
            str - Selected mode or action
        """
        for action, btn, _ in self.buttons:
            if btn.is_clicked(mouse_pos, True):
                return action
        return None
    
    def draw(self, surface, font_large, font_medium, font_small):
        """Draw mode selection menu"""
        surface.fill(COLOR_WHITE)
        
        title = font_large.render("SELECT GAME MODE", True, COLOR_PURPLE)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=30)
        surface.blit(title, title_rect)
        
        # Draw buttons with descriptions
        for _, btn, description in self.buttons:
            btn.draw(surface, font_medium)
            
            # Draw descriptions under mode buttons (not back button)
            if description:
                desc_surf = font_small.render(description, True, COLOR_DARK_GREY)
                desc_rect = desc_surf.get_rect(centerx=btn.rect.centerx, 
                                               y=btn.rect.bottom + 5)
                surface.blit(desc_surf, desc_rect)


class QuestionCountMenu:
    """
    Menu for selecting number of questions
    Only available in Classic mode
    """
    
    def __init__(self, mode):
        """
        Initialize question count selection
        
        Args:
            mode: str - Game mode (determines max questions)
        """
        self.mode = mode
        self.number_input = NumberInput(
            SCREEN_WIDTH // 2 - 75,
            SCREEN_HEIGHT // 2 - 25,
            150,
            50,
            DEFAULT_QUESTION_COUNT
        )
        
        # Create buttons
        self.start_btn = Button(
            SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 70, 150, 50,
            "START",
            base_color=COLOR_GREEN,
            hover_color=COLOR_LIGHT_GREEN,
            click_color=COLOR_DARK_GREEN
        )
        
        self.back_btn = Button(
            30, SCREEN_HEIGHT - 70, 100, 50,
            "BACK",
            base_color=COLOR_LIGHT_GREY,
            hover_color=COLOR_MEDIUM_GREY,
            click_color=COLOR_DARK_GREY
        )
    
    def handle_event(self, event):
        """
        Handle keyboard input
        
        Args:
            event: pygame.event.Event - Input event
        """
        self.number_input.handle_event(event)
    
    def update(self, mouse_pos, mouse_clicked):
        """Update button states"""
        self.start_btn.update(mouse_pos, mouse_clicked)
        self.back_btn.update(mouse_pos, mouse_clicked)
    
    def handle_click(self, mouse_pos):
        """
        Handle click events
        
        Returns:
            str or int - "back", or number of questions to start
        """
        if self.back_btn.is_clicked(mouse_pos, True):
            return "back"
        if self.start_btn.is_clicked(mouse_pos, True):
            return self.number_input.get_value()
        return None
    
    def draw(self, surface, font_large, font_medium):
        """Draw question count selection menu"""
        surface.fill(COLOR_WHITE)
        
        title = font_large.render("SELECT QUESTION COUNT", True, COLOR_PURPLE)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=50)
        surface.blit(title, title_rect)
        
        label = font_medium.render("Questions:", True, COLOR_BLACK)
        label_rect = label.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 - 50)
        surface.blit(label, label_rect)
        
        self.number_input.draw(surface, font_medium)
        self.start_btn.draw(surface, font_medium)
        self.back_btn.draw(surface, font_medium)
        
        # Draw range hint
        hint = font_medium.render(f"(1-{MAX_QUESTION_COUNT})", True, COLOR_DARK_GREY)
        hint_rect = hint.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 + 25)
        surface.blit(hint, hint_rect)


class PauseMenu:
    """
    In-game pause menu
    Displayed when ESC is pressed during gameplay
    """
    
    def __init__(self):
        """Initialize pause menu"""
        self.resume_btn = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50,
            "RESUME",
            base_color=COLOR_GREEN,
            hover_color=COLOR_LIGHT_GREEN,
            click_color=COLOR_DARK_GREEN
        )
        
        self.quit_btn = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50,
            "QUIT TO MENU",
            base_color=COLOR_RED,
            hover_color=COLOR_LIGHT_RED,
            click_color=COLOR_DARK_RED
        )
    
    def update(self, mouse_pos, mouse_clicked):
        """Update button states"""
        self.resume_btn.update(mouse_pos, mouse_clicked)
        self.quit_btn.update(mouse_pos, mouse_clicked)
    
    def handle_click(self, mouse_pos):
        """
        Handle click on pause menu
        
        Returns:
            str - "resume" or "quit"
        """
        if self.resume_btn.is_clicked(mouse_pos, True):
            return "resume"
        if self.quit_btn.is_clicked(mouse_pos, True):
            return "quit"
        return None
    
    def draw(self, surface, font_large, font_medium):
        """
        Draw semi-transparent pause menu overlay
        
        Args:
            surface: pygame.Surface - Game surface
            font_large: pygame.font.Font - Large font
            font_medium: pygame.font.Font - Medium font
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLOR_BLACK)
        surface.blit(overlay, (0, 0))
        
        # Draw pause menu box
        menu_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT // 2 - 130,
            300,
            260
        )
        pygame.draw.rect(surface, COLOR_LIGHT_GREY, menu_rect)
        pygame.draw.rect(surface, COLOR_BLACK, menu_rect, 5)
        
        # Draw title
        title = font_large.render("PAUSED", True, COLOR_PURPLE)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 - 110)
        surface.blit(title, title_rect)
        
        # Draw buttons
        self.resume_btn.draw(surface, font_medium)
        self.quit_btn.draw(surface, font_medium)


class ResultsScreen:
    """
    Results screen displayed after quiz completion
    Shows score, grade, and statistics
    """
    
    def __init__(self, results):
        """
        Initialize results screen
        
        Args:
            results: dict - Results data from quiz
        """
        self.results = results
        self.restart_btn = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50,
            "RESTART",
            base_color=COLOR_GREEN,
            hover_color=COLOR_LIGHT_GREEN,
            click_color=COLOR_DARK_GREEN
        )
        
        self.menu_btn = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 40, 200, 50,
            "MAIN MENU",
            base_color=COLOR_BLUE,
            hover_color=COLOR_CYAN,
            click_color=COLOR_DARK_PURPLE
        )
    
    def update(self, mouse_pos, mouse_clicked):
        """Update button states"""
        self.restart_btn.update(mouse_pos, mouse_clicked)
        self.menu_btn.update(mouse_pos, mouse_clicked)
    
    def handle_click(self, mouse_pos):
        """
        Handle click on results screen
        
        Returns:
            str - "restart" or "menu"
        """
        if self.restart_btn.is_clicked(mouse_pos, True):
            return "restart"
        if self.menu_btn.is_clicked(mouse_pos, True):
            return "menu"
        return None
    
    def draw(self, surface, font_large, font_medium, font_small):
        """
        Draw results screen with score and statistics
        
        Args:
            surface: pygame.Surface - Surface to draw on
            font_large: pygame.font.Font - Large font
            font_medium: pygame.font.Font - Medium font
            font_small: pygame.font.Font - Small font
        """
        surface.fill(COLOR_WHITE)
        
        # Title
        title = font_large.render("QUIZ COMPLETE!", True, COLOR_PURPLE)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=50)
        surface.blit(title, title_rect)
        
        # Score
        score_text = font_medium.render(
            f"Score: {self.results['score']}/{self.results['total']}",
            True, COLOR_BLACK
        )
        score_rect = score_text.get_rect(centerx=SCREEN_WIDTH // 2, y=150)
        surface.blit(score_text, score_rect)
        
        # Percentage
        percentage_text = font_large.render(
            f"{self.results['percentage']:.1f}%",
            True, COLOR_BLUE
        )
        percentage_rect = percentage_text.get_rect(centerx=SCREEN_WIDTH // 2, y=220)
        surface.blit(percentage_text, percentage_rect)
        
        # Grade
        grade_color = COLOR_GREEN if self.results['percentage'] >= 70 else COLOR_RED
        grade_text = font_large.render(
            f"Grade: {self.results['grade']}",
            True, grade_color
        )
        grade_rect = grade_text.get_rect(centerx=SCREEN_WIDTH // 2, y=290)
        surface.blit(grade_text, grade_rect)
        
        # Mode and time
        mode_text = font_small.render(f"Mode: {self.results['mode']}", True, COLOR_DARK_GREY)
        mode_rect = mode_text.get_rect(centerx=SCREEN_WIDTH // 2, y=370)
        surface.blit(mode_text, mode_rect)
        
        time_text = font_small.render(f"Time: {self.results['time']} seconds", True, COLOR_DARK_GREY)
        time_rect = time_text.get_rect(centerx=SCREEN_WIDTH // 2, y=400)
        surface.blit(time_text, time_rect)
        
        # Buttons
        self.restart_btn.draw(surface, font_medium)
        self.menu_btn.draw(surface, font_medium)