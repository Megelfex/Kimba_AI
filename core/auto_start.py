from core.auto_analyzer import start_auto_analyzer_in_background
from core.auto_executor import start_auto_executor_in_background
from core.goal_manager import start_goal_manager_in_background
from core.auto_overlay_mood import start_auto_overlay_mood_in_background

def start_all_background_services():
    """Startet alle Hintergrunddienste für Kimba."""
    start_auto_analyzer_in_background()
    start_auto_executor_in_background()
    start_goal_manager_in_background()
    start_auto_overlay_mood_in_background()
