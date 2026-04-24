"""
CONSTANTS AND CONFIGURATION FOR RUSSIAN HISTORY QUIZ
Pixel art inspired game - All colors, game modes, and settings defined here
"""

# ============== SCREEN DIMENSIONS ==============
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# ============== PIXEL ART COLORS ==============
# Primary colors - retro pixel art palette
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_DARK_GREY = (50, 50, 50)
COLOR_LIGHT_GREY = (200, 200, 200)
COLOR_MEDIUM_GREY = (150, 150, 150)

# Primary palette - vibrant pixel art
COLOR_PURPLE = (102, 126, 234)
COLOR_DARK_PURPLE = (118, 75, 162)
COLOR_LIGHT_PURPLE = (200, 150, 255)

COLOR_GREEN = (40, 167, 69)
COLOR_LIGHT_GREEN = (212, 237, 218)
COLOR_DARK_GREEN = (20, 100, 40)

COLOR_RED = (220, 53, 69)
COLOR_LIGHT_RED = (248, 215, 218)
COLOR_DARK_RED = (150, 30, 40)

COLOR_YELLOW = (255, 193, 7)
COLOR_ORANGE = (255, 140, 0)
COLOR_BLUE = (0, 150, 200)
COLOR_CYAN = (100, 200, 255)

# ============== GAME MODES ==============
class GameMode:
    """Enum for different game modes"""
    CLASSIC = "CLASSIC"  # Standard quiz mode
    SUDDEN_DEATH = "SUDDEN_DEATH"  # Lose on first wrong answer
    MARATHON = "MARATHON"  # Complete all questions until 100% correct

# ============== GAME STATES ==============
class GameState:
    """Enum for game state management"""
    MAIN_MENU = "MAIN_MENU"
    MODE_SELECTION = "MODE_SELECTION"
    QUESTION_COUNT = "QUESTION_COUNT"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    RESULTS = "RESULTS"
    GAME_OVER = "GAME_OVER"

# ============== FONT SIZES ==============
FONT_SIZE_HUGE = 48
FONT_SIZE_LARGE = 32
FONT_SIZE_MEDIUM = 24
FONT_SIZE_SMALL = 18
FONT_SIZE_TINY = 12

# ============== BUTTON SIZES ==============
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_SMALL_WIDTH = 100
BUTTON_SMALL_HEIGHT = 40

# ============== ANSWER BUTTON SIZES ==============
ANSWER_BUTTON_WIDTH = 350
ANSWER_BUTTON_HEIGHT = 60
ANSWER_BUTTON_GAP = 30

# ============== TIMING ==============
QUESTION_TIMER_SECONDS = 60  # Time limit per question
PAUSE_MENU_APPEAR_TIME = 0.3  # Animation time for pause menu

# ============== DEFAULT VALUES ==============
DEFAULT_QUESTION_COUNT = 100
MAX_QUESTION_COUNT = 1000
MIN_QUESTION_COUNT = 1
