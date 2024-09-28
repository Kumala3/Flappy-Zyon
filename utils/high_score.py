"""
high_score.py

Handles loading and saving the high score.
"""


def load_high_score() -> None:
    """
    Load the high score from a file.
    """
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


def save_high_score(score: int) -> None:
    """
    Save the high score to a file.
    """
    with open("high_score.txt", "w") as file:
        file.write(str(score))
