import random
import os
import time
import threading
import keyboard
from colorama import init, Fore, Style

init(autoreset=True)

bar_length = 10
progress = 5
number_to_guess = random.randint(1, 10)
money = 10
help_used = 0
user_guess = None
lock = threading.Lock()

menu_items = ["Start", "Store", "About Us", "Exit"]
selected_index = 0

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def center_text(text, width=80):
    spaces = (width - len(text)) // 2
    return ' ' * spaces + text

def draw_menu(selected):
    clear()
    print("\n" * 5)
    for i, item in enumerate(menu_items):
        if i == selected:
            color = Fore.GREEN if item == "Start" else (Fore.RED if item == "Exit" else Fore.CYAN)
            print(center_text(color + f"[::::: {item} :::::]" + Style.RESET_ALL))
        else:
            print(center_text(f"[::::: {item} :::::]"))

def menu():
    global selected_index
    draw_menu(selected_index)
    while True:
        if keyboard.is_pressed("up"):
            selected_index = (selected_index - 1) % len(menu_items)
            draw_menu(selected_index)
            time.sleep(0.15)
        elif keyboard.is_pressed("down"):
            selected_index = (selected_index + 1) % len(menu_items)
            draw_menu(selected_index)
            time.sleep(0.15)
        elif keyboard.is_pressed("enter"):
            option = menu_items[selected_index]
            if option == "Start":
                difficulty = difficulty_menu()
                if difficulty:
                    play(difficulty)
                draw_menu(selected_index)
            elif option == "Exit":
                print(Fore.RED + "\nExiting game...")
                time.sleep(1)
                exit()
            elif option == "Store":
                clear()
                print(Fore.MAGENTA + "\n🛒 Store is under construction!")
                input("\nPress Enter to return to menu...")
                draw_menu(selected_index)
            elif option == "About Us":
                clear()
                print(Fore.YELLOW + "\n👨‍💻 This game was made with Python and love!")
                input("\nPress Enter to return to menu...")
                draw_menu(selected_index)

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

def difficulty_menu():
    options = ["easy"]
    selected = 0
    while True:
        clear()
        print("\n" * 5)
        for i, item in enumerate(options):
            if i == selected:
                print(center_text(Fore.GREEN + f"[::::: {item} :::::]" + Style.RESET_ALL))
            else:
                print(center_text(f"[::::: {item} :::::]"))
        if keyboard.is_pressed("up") or keyboard.is_pressed("down"):
            # چون فقط یه گزینه هست، هیچ کاری نمیکنه ولی برای توسعه آماده است
            time.sleep(0.15)
        elif keyboard.is_pressed("enter"):
            return options[selected]
        time.sleep(0.1)

def play(difficulty):
    global progress, number_to_guess, money, help_used, user_guess

    # بسته به سختی عدد حد بالا تغییر کنه (فعلاً فقط easy هست)
    if difficulty == "easy":
        max_number = 10
    else:
        max_number = 10

    progress = 5
    number_to_guess = random.randint(1, max_number)
    money = 10
    help_used = 0
    user_guess = None

    threading.Thread(target=listen_for_hint, daemon=True).start()

    while True:
        clear()
        print(f"🎮 Number Guessing Game ({difficulty.title()}) - Guess number between 1 and {max_number}")
        print(f"💰 Money: {money} | 💡 Helps used: {help_used}")
        draw_bar(progress)

        if progress >= bar_length:
            print(Fore.GREEN + "\n🎉 You Win! Well done!")
            input("\nPress Enter to return to menu...")
            return
        elif progress <= 0:
            print(Fore.RED + "\n💥 Game Over! You lost.")
            input("\nPress Enter to return to menu...")
            return

        try:
            user_guess = int(input("🔢 Enter your guess (or 99 to return to menu): "))
            if user_guess == 99:
                print(Fore.CYAN + "🔁 Returning to main menu...")
                time.sleep(1)
                return

            if user_guess == number_to_guess:
                print(Fore.GREEN + "✅ Correct!")
                progress += 1
                draw_bar(progress, 'correct')
                number_to_guess = random.randint(1, max_number)
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
        action = menu()
        if action == "start":
            # play() را با سختی فراخوانی می‌کنیم
            pass
