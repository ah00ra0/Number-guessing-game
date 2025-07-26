import random
import os
import time
from colorama import init, Fore, Style

init(autoreset=True)

bar_length = 10
progress = 5  # شروع از وسط
number_to_guess = random.randint(1, 10)

def draw_bar(progress, last_result=None):
    bar = ''
    for i in range(bar_length):
        if i < progress:
            if last_result == 'correct':
                bar += Fore.GREEN + '█'
            elif last_result == 'wrong':
                bar += Fore.RED + '█'
            else:
                bar += Fore.WHITE + '█'
        else:
            bar += Fore.WHITE + '░'
    print(f"[{bar}]" + Style.RESET_ALL)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def play():
    global progress, number_to_guess
    while True:
        clear()
        print("Number Guessing Game (1 to 10)")
        draw_bar(progress)

        if progress >= bar_length:
            print(Fore.GREEN + "\n🎉 You Win! Well done!")
            break
        elif progress <= 0:
            print(Fore.RED + "\n💥 Game Over! You lost.")
            break

        try:
            guess = int(input("Enter your guess: "))
            if guess == 99:
                print("Exiting...")
                break
            if guess == number_to_guess:
                print(Fore.GREEN + "Correct!")
                progress += 1
                draw_bar(progress, 'correct')
            else:
                print(Fore.RED + f"Wrong! The number was {number_to_guess}")
                progress -= 1
                draw_bar(progress, 'wrong')
            number_to_guess = random.randint(1, 10)
            time.sleep(1.5)
        except ValueError:
            print("Please enter a valid number!")
            time.sleep(1)

if __name__ == "__main__":
    play()
