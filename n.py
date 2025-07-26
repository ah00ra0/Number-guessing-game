import random
import os
import time
import threading
import keyboard
from colorama import init, Fore, Style

init(autoreset=True)

progress = 0
number_to_guess = None
money = 10
help_used = 0
user_guess = None
lock = threading.Lock()

menu_items = ["Start", "Store", "About Us", "Exit"]
difficulty_options = ["easy", "normal", "hard", "mod"]
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
            if item == "Start":
                color = Fore.GREEN
            elif item == "Exit":
                color = Fore.RED
            else:
                color = Fore.CYAN
            print(center_text(color + f"[::::: {item} :::::]" + Style.RESET_ALL))
        else:
            print(center_text(f"[::::: {item} :::::]"))

def menu():
    global selected_index
    draw_menu(selected_index)
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "up":
                selected_index = (selected_index - 1) % len(menu_items)
                draw_menu(selected_index)
            elif event.name == "down":
                selected_index = (selected_index + 1) % len(menu_items)
                draw_menu(selected_index)
            elif event.name == "space":   # انتخاب با Space
                return menu_items[selected_index]

def draw_difficulty_menu(selected):
    clear()
    print("\n" * 5)
    for i, item in enumerate(difficulty_options):
        if i == selected:
            print(center_text(Fore.GREEN + f"[::::: {item} :::::]" + Style.RESET_ALL))
        else:
            print(center_text(f"[::::: {item} :::::]"))

def difficulty_menu():
    selected = 0
    draw_difficulty_menu(selected)
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "up":
                selected = (selected - 1) % len(difficulty_options)
                draw_difficulty_menu(selected)
            elif event.name == "down":
                selected = (selected + 1) % len(difficulty_options)
                draw_difficulty_menu(selected)
            elif event.name == "space":  # انتخاب با Space
                return difficulty_options[selected]

def draw_bar(progress, bar_length, last_result=None):
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
    global money, help_used, user_guess, number_to_guess
    if money != float('inf') and money <= 0:
        print(Fore.RED + "\nYou don't have enough money to get a hint.")
        return
    if user_guess is not None:
        if money != float('inf'):
            money -= 1
        help_used += 1
        hint = "larger" if number_to_guess > user_guess else "smaller"
        print(Fore.YELLOW + f"\nHint: Your guess was {user_guess} → The number is {hint}.")
    else:
        print(Fore.CYAN + "\nMake a guess first to get a hint.")

def listen_for_hint():
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "y" and keyboard.is_pressed("ctrl"):
                with lock:
                    give_hint()
                    time.sleep(1)

def play(difficulty):
    global progress, number_to_guess, money, help_used, user_guess

    if difficulty == "easy":
        bar_length = 6          # طول نوار 6
        progress = 3            # شروع وسط نوار
        money = 10
        max_number = 1          # عدد بین 0 و 1
    elif difficulty == "normal":
        bar_length = 6
        progress = 3
        money = 10
        max_number = 10
    elif difficulty == "hard":
        bar_length = 10
        progress = 5
        money = 10
        max_number = 10
    elif difficulty == "mod":
        bar_length = 10
        progress = 5
        money = float('inf')
        max_number = 10
    else:
        bar_length = 10
        progress = 5
        money = 10
        max_number = 10

    # عدد اولیه حدس
    number_to_guess = random.choice([0, 1]) if difficulty == "easy" else random.randint(0, max_number)
    help_used = 0
    user_guess = None

    while True:
        clear()
        print(f"🎮 Number Guessing Game ({difficulty.title()}) - Guess number between 0 and {max_number if difficulty != 'easy' else 1}")
        print(f"💰 Money: {'∞' if money == float('inf') else money} | 💡 Helps used: {help_used}")
        draw_bar(progress, bar_length)

        if progress >= bar_length:
            print(Fore.GREEN + "\n🎉 You Win! Well done!")
            input("\nPress Enter to return to menu...")
            return
        elif progress <= 0:
            print(Fore.RED + "\n💥 Game Over! You lost.")
            input("\nPress Enter to return to menu...")
            return

        try:
            guess_input = input("🔢 Enter your guess (or 99 to return to menu): ")
            user_guess = int(guess_input)
            if user_guess == 99:
                print(Fore.CYAN + "🔁 Returning to main menu...")
                time.sleep(1)
                return

            if user_guess == number_to_guess:
                print(Fore.GREEN + f"✅ Correct! The number was {number_to_guess}.")
                progress += 1
                # عدد جدید وقتی درست حدس زدی:
                number_to_guess = random.choice([0, 1]) if difficulty == "easy" else random.randint(0, max_number)
                draw_bar(progress, bar_length, 'correct')
            else:
                print(Fore.RED + f"❌ Wrong guess! Your guess: {user_guess}, Number was {number_to_guess}.")
                progress -= 1
                draw_bar(progress, bar_length, 'wrong')

            time.sleep(1.5)
        except ValueError:
            print("⛔ Please enter a valid number.")
            time.sleep(1)

if __name__ == "__main__":
    hint_thread = threading.Thread(target=listen_for_hint, daemon=True)
    hint_thread.start()

    while True:
        choice = menu()
        if choice == "Start":
            diff = difficulty_menu()
            play(diff)
        elif choice == "Exit":
            print(Fore.RED + "\nExiting game... Goodbye!")
            time.sleep(1)
            break
        elif choice == "Store":
            clear()
            print(Fore.MAGENTA + "\n🛒 Store is under construction! Press Enter to return.")
            input()
        elif choice == "About Us":
            clear()
            print(Fore.YELLOW + "\n👨‍💻 This game was made with Python and love! Press Enter to return.")
            input()
