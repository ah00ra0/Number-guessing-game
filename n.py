import random
import os
import time
import threading
import keyboard
from colorama import init, Fore, Style

init(autoreset=True)

# تنظیمات نوار
bar_length = 10
progress = 5
number_to_guess = random.randint(1, 10)
money = 10
help_used = 0
user_guess = None

lock = threading.Lock()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def center_text(text, width=80):
    spaces = (width - len(text)) // 2
    return ' ' * spaces + text

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

def give_hint():
    global money, help_used
    if money > 0 and user_guess is not None:
        money -= 1
        help_used += 1
        hint = "larger" if number_to_guess > user_guess else "smaller"
        print(Fore.YELLOW + f"\nHint: Your guess was {user_guess} → The number is {hint}.")
    elif money <= 0:
        print(Fore.RED + "\nYou don't have enough money to get a hint.")
    else:
        print(Fore.CYAN + "\nMake a guess first to get a hint.")

def listen_for_hint():
    while True:
        if keyboard.is_pressed("ctrl+y"):
            with lock:
                give_hint()
                time.sleep(1)

def show_menu():
    clear()
    print("\n" * 5)
    print(center_text("[::::::start::::::]"))
    print(center_text("Press Enter to start..."))
    while True:
        if keyboard.is_pressed("enter"):
            time.sleep(0.5)
            break

def play():
    global progress, number_to_guess, money, help_used, user_guess

    # مقداردهی دوباره برای شروع جدید
    progress = 5
    number_to_guess = random.randint(1, 10)
    money = 10
    help_used = 0
    user_guess = None

    threading.Thread(target=listen_for_hint, daemon=True).start()

    while True:
        clear()
        print(f"🎮 Number Guessing Game (1 to 10)")
        print(f"💰 Money: {money} | 💡 Helps used: {help_used}")
        draw_bar(progress)

        if progress >= bar_length:
            print(Fore.GREEN + "\n🎉 You Win! Well done!")
            break
        elif progress <= 0:
            print(Fore.RED + "\n💥 Game Over! You lost.")
            break

        try:
            user_guess = int(input("🔢 Enter your guess (or 99 to quit): "))
            if user_guess == 99:
                print("Exiting...")
                exit()

            if user_guess == number_to_guess:
                print(Fore.GREEN + "✅ Correct!")
                progress += 1
                draw_bar(progress, 'correct')
                number_to_guess = random.randint(1, 10)
            else:
                print(Fore.RED + "❌ Wrong guess!")
                progress -= 1
                draw_bar(progress, 'wrong')

            time.sleep(1.5)
        except ValueError:
            print("⛔ Please enter a valid number.")
            time.sleep(1)

if __name__ == "__main__":
    while True:
        show_menu()
        play()
