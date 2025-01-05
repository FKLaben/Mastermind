import random
from typing import List, Tuple
import sys
from dataclasses import dataclass

@dataclass
class GameConfig:
    """Stores game configuration settings"""
    COLORS: List[str] = None
    CODE_LENGTH: int = 4
    MAX_TRIES: int = 10
    
    def __post_init__(self):
        if self.COLORS is None:
            self.COLORS = ['R', 'G', 'B', 'Y', 'W', 'O']  # Red, Green, Blue, Yellow, White, Orange

class MastermindGame:
    """Main game class implementing the Mastermind logic"""
    
    def __init__(self, config: GameConfig = None):
        """Initialize the game with optional custom configuration"""
        self.config = config or GameConfig()
        self.secret_code = self._generate_secret_code()
        self.tries = 0
        self.game_won = False
    
    def _generate_secret_code(self) -> List[str]:
        """Generate a random secret code using available colors"""
        return random.choices(self.config.COLORS, k=self.config.CODE_LENGTH)
    
    def _validate_guess(self, guess: str) -> bool:
        """Validate if the guess is in correct format"""
        if len(guess) != self.config.CODE_LENGTH:
            return False
        return all(color.upper() in self.config.COLORS for color in guess)
    
    def _evaluate_guess(self, guess: List[str]) -> Tuple[int, int]:
        """
        Evaluate a guess and return the number of exact and color matches
        Returns: Tuple of (exact_matches, color_matches)
        """
        exact_matches = 0
        color_matches = 0
        
        # Create copies to avoid modifying original lists
        secret_copy = self.secret_code.copy()
        guess_copy = guess.copy()
        
        # First count exact matches
        for i in range(len(secret_copy)):
            if guess_copy[i] == secret_copy[i]:
                exact_matches += 1
                secret_copy[i] = guess_copy[i] = None
        
        # Then count color matches
        for i in range(len(guess_copy)):
            if guess_copy[i] is not None and guess_copy[i] in secret_copy:
                color_matches += 1
                secret_copy[secret_copy.index(guess_copy[i])] = None
        
        return exact_matches, color_matches
    
    def play_turn(self, guess: str) -> Tuple[bool, str]:
        """
        Play a single turn of the game
        Returns: Tuple of (is_valid_guess, feedback_message)
        """
        guess = guess.upper()
        if not self._validate_guess(guess):
            return False, "Invalid guess! Please use valid colors and correct length."
        
        self.tries += 1
        exact_matches, color_matches = self._evaluate_guess(list(guess))
        
        if exact_matches == self.config.CODE_LENGTH:
            self.game_won = True
            return True, f"Congratulations! You've won in {self.tries} tries!"
        
        if self.tries >= self.config.MAX_TRIES:
            return True, f"Game Over! The secret code was {''.join(self.secret_code)}"
        
        return True, f"Exact matches: {exact_matches}, Color matches: {color_matches}"

def print_instructions(config: GameConfig):
    """Print game instructions"""
    print("\n=== MASTERMIND ===")
    print("\nTry to guess the secret code!")
    print(f"Available colors: {', '.join(config.COLORS)}")
    print(f"Code length: {config.CODE_LENGTH}")
    print(f"Maximum tries: {config.MAX_TRIES}")
    print("\nEnter your guess using color initials (e.g., RGBY)")
    print("Press 'q' to quit the game")
    print("=" * 20 + "\n")

def main():
    """Main game loop"""
    game = MastermindGame()
    print_instructions(game.config)
    
    while not game.game_won and game.tries < game.config.MAX_TRIES:
        guess = input(f"\nEnter guess #{game.tries + 1}: ").strip()
        
        if guess.lower() == 'q':
            print("Thanks for playing!")
            sys.exit(0)
        
        is_valid, feedback = game.play_turn(guess)
        print(feedback)

if __name__ == "__main__":
    main()