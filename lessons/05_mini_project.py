"""
Mini Project: Number Guessing Game
----------------------------------
Concepts used: variables, input, conditionals, loops, functions, random numbers.
"""

import random


def pick_secret_number(low: int = 1, high: int = 10) -> int:
    """Return a random number between low and high (inclusive)."""
    return random.randint(low, high)


def get_guess() -> int:
    """Prompt the user for a number and convert it to int."""
    guess_text = input("Enter your guess: ")
    return int(guess_text)


def play_round():
    secret = pick_secret_number()
    attempts_left = 3

    print("I'm thinking of a number between 1 and 10.")

    while attempts_left > 0:
        print(f"You have {attempts_left} attempts.")
        guess = get_guess()

        if guess == secret:
            print("You got it!")
            return
        elif guess < secret:
            print("Too low.")
        else:
            print("Too high.")

        attempts_left -= 1

    print(f"Sorry, the number was {secret}. Better luck next time.")


def main():
    play_again = "yes"
    while play_again.lower().startswith("y"):
        play_round()
        play_again = input("Play again? (yes/no): ")
    print("Thanks for playing!")


if __name__ == "__main__":
    main()

# --- Your turn --------------------------------------------------------------
# 1. Add input validation so the program doesn't crash on non-number guesses.
# 2. Let the user choose the range and number of attempts.
# 3. Track how many games the user wins vs. loses.

