import random
def play_game():
    secret = random.randint(1, 100)
    attempts = 7
    print("Guess the number between 1 and 100. You have 7 attempts.")
    for i in range(1, attempts + 1):
        try:
            guess = int(input(f"Attempt {i}: "))
        except ValueError:
            print("Invalid input. Enter an integer.")
            continue
        if guess < secret:
            print("Too low!")
        elif guess > secret:
            print("Too high!")
        else:
            print(f"Correct! You won in {i} attempts.")
            return
    print(f"Game over! The number was {secret}.")
play_game()