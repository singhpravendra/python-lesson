'''
Guess Number Game - Thsi is a simple game to guess a number between 1 and 10.
The user has 3 attempts to guess the number.
If  user guess the number in less than 3 attempts, user wins the game.
else user loses the game.
'''

import random

def secret_number_1(min: int = 0, max: int = 10) -> int:
    return random.randint(min, max)

def guess_number() -> int:
    num = input("Enter your guess: ")
    return int(num)

def play_game():
    secret_number = secret_number_1()
    attempts_left = 3

    print("Guese the number between 0 and 10")

    while attempts_left > 0:
       print(f"you have {attempts_left} attempts left")
       guess = guess_number()
       if guess == secret_number:
           print("You guessed the number!")
           return
       elif guess < secret_number:
           print("Too low.")
       else:
           print("Too high.")
       attempts_left -= 1
    print(f"You lost the game! The number was {secret_number}")
    return


def main():
    play_again = input("Do you want to play the game: ")
    if play_again.startswith("y"):
        play_game()
    else:
        print("The End")


if __name__ == "__main__":
    main()
