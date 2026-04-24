"""
UI COMPONENTS - Pixel Art Inspired Interface Elements
Reusable button and input components with pixel art aesthetic
"""

import pygame
from constants import *

class Button:
    """
    Pixel art styled button with hover effects and click detection
    
    Attributes:
        rect: pygame.Rect - Button position and size
        text: str - Button display text
        color: tuple - Current button color
        base_color: tuple - Default button color
        hover_color: tuple - Color when mouse hovers
        click_color: tuple - Color when clicked
        hovered: bool - Whether mouse is over button
    """
    
    def __init__(self, x, y, width, height, text, base_color=COLOR_LIGHT_GREY, 
                 hover_color=COLOR_PURPLE, click_color=COLOR_DARK_PURPLE):
        """
        Initialize a new button
        
        Args:
            x: X position on screen
            y: Y position on screen
            width: Button width in pixels
            height: Button height in pixels
            text: Text to display on button
            base_color: Default button color (RGB tuple)
            hover_color: Color when hovering (RGB tuple)
            click_color: Color when clicked (RGB tuple)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.color = base_color
        self.hovered = False
        self.clicked = False
    
    def update(self, mouse_pos, mouse_clicked=False):
        """
        Update button state based on mouse position and clicks
        
        Args:
            mouse_pos: tuple (x, y) - Current mouse position
            mouse_clicked: bool - Whether mouse button is pressed
        """
        # Check if mouse is over button (pixel perfect collision)
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Update color based on hover state
        if self.hovered:
            self.color = self.hover_color if not mouse_clicked else self.click_color
        else:
            self.color = self.base_color
    
    def is_clicked(self, mouse_pos, mouse_pressed):
        """
        Check if button was clicked
        
        Args:
            mouse_pos: tuple (x, y) - Current mouse position
            mouse_pressed: bool - Whether mouse button is pressed
            
        Returns:
            bool - True if button was clicked
        """
        return self.rect.collidepoint(mouse_pos) and mouse_pressed
    
    def draw(self, surface, font):
        """
        Draw button with pixel art aesthetic (blocky borders)
        
        Args:
            surface: pygame.Surface - Surface to draw on
            font: pygame.font.Font - Font for rendering text
        """
        # Draw main button rectangle with thick border (pixel art style)
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, COLOR_BLACK, self.rect, 3)  # 3px border for pixel art
        
        # Render and center text on button
        text_surface = font.render(self.text, True, COLOR_BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class AnswerButton(Button):
    """
    Specialized button for quiz answers with correct/incorrect states
    
    Attributes:
        is_correct: bool - Whether this is the correct answer
        state: str - Current state (normal, selected, evaluated)
    """
    
    def __init__(self, x, y, width, height, text, is_correct):
        """
        Initialize answer button
        
        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            text: Answer text
            is_correct: Whether this is the correct answer
        """
        super().__init__(x, y, width, height, text, 
                        base_color=COLOR_LIGHT_GREY,
                        hover_color=COLOR_PURPLE,
                        click_color=COLOR_DARK_PURPLE)
        self.is_correct = is_correct
        self.state = "normal"  # normal, selected, evaluated
        self.selected = False
    
    def set_state(self, state):
        """
        Set the button's visual state
        
        Args:
            state: str - "normal", "selected", or "evaluated"
        """
        self.state = state
        
        # Update colors based on state
        if state == "normal":
            self.color = self.base_color
        elif state == "selected":
            self.color = self.hover_color
        elif state == "evaluated":
            # Show correct/incorrect coloring after answer
            self.color = COLOR_LIGHT_GREEN if self.is_correct else COLOR_LIGHT_RED
    
    def draw(self, surface, font):
        """
        Draw answer button with appropriate state coloring
        
        Args:
            surface: pygame.Surface - Surface to draw on
            font: pygame.font.Font - Font for rendering text
        """
        # Draw button rectangle with thick border
        pygame.draw.rect(surface, self.color, self.rect)
        
        # Different border color for evaluated state
        border_color = COLOR_GREEN if (self.state == "evaluated" and self.is_correct) else COLOR_BLACK
        if self.state == "evaluated" and not self.is_correct:
            border_color = COLOR_RED
        
        pygame.draw.rect(surface, border_color, self.rect, 3)
        
        # Render text with word wrapping for long answers
        text_lines = self._wrap_text(self.text, font)
        line_height = font.get_height() + 2
        
        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, COLOR_BLACK)
            text_x = self.rect.x + 10
            text_y = self.rect.y + 10 + (i * line_height)
            surface.blit(text_surface, (text_x, text_y))
    
    def _wrap_text(self, text, font, max_width=320):
        """
        Wrap text to fit within button width
        
        Args:
            text: str - Text to wrap
            font: pygame.font.Font - Font for measuring
            max_width: int - Maximum width before wrapping
            
        Returns:
            list - Lines of wrapped text
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


class NumberInput:
    """
    Text input for selecting number of questions
    Allows user to type and modify the question count
    """
    
    def __init__(self, x, y, width, height, initial_value=DEFAULT_QUESTION_COUNT):
        """
        Initialize number input field
        
        Args:
            x: X position
            y: Y position
            width: Input width
            height: Input height
            initial_value: Starting number value
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.value = str(initial_value)
        self.active = False
        self.cursor_pos = len(self.value)
    
    def handle_event(self, event):
        """
        Handle keyboard input for the number field
        
        Args:
            event: pygame.event.Event - Input event to process
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Remove last character
                self.value = self.value[:-1]
                self.cursor_pos = max(0, self.cursor_pos - 1)
            elif event.unicode.isdigit():
                # Only allow digits
                num = int(self.value + event.unicode) if self.value else int(event.unicode)
                
                # Keep within bounds
                if num <= MAX_QUESTION_COUNT:
                    self.value = str(num)
                    self.cursor_pos = len(self.value)
    
    def get_value(self):
        """
        Get the current numeric value
        
        Returns:
            int - Numeric value in input field
        """
        return int(self.value) if self.value else MIN_QUESTION_COUNT
    
    def draw(self, surface, font):
        """
        Draw the number input field with pixel art style
        
        Args:
            surface: pygame.Surface - Surface to draw on
            font: pygame.font.Font - Font for rendering
        """
        # Draw input background and border
        pygame.draw.rect(surface, COLOR_WHITE, self.rect)
        pygame.draw.rect(surface, COLOR_DARK_GREY if self.active else COLOR_BLACK, self.rect, 3)
        
        # Render the value text
        text_surface = font.render(self.value, True, COLOR_BLACK)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 5, self.rect.centery))
        surface.blit(text_surface, text_rect)