import random
import os
import time
import keyboard  # برای کنترل ترکیب کلیدها
from colorama import init, Fore, Style

init(autoreset=True)

bar_length = 10
progress = 5  # شروع از وسط
number_to_guess = random.randint(1, 10)
money = 10  # شروع با 10 پول
help_used = 0  # تعداد کمک‌هایی که استفاده شده

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

def give_hint():
    global money
    if money > 0:
        money -= 1  # کم کردن یک پول برای استفاده از کمک
        hint = "larger" if number_to_guess > user_guess else "smaller"
        print(f"\nHint: The number is {hint} than your guess.")
    else:
        print("\nYou don't have enough money for a hint!")

def play():
    global progress, number_to_guess, money, help_used
    while True:
        clear()
        print(f"Number Guessing Game (1 to 10) | Money: {money} | Helps used: {help_used}")
        draw_bar(progress)

        if progress >= bar_length:
            print(Fore.GREEN + "\n🎉 You Win! Well done!")
            break
        elif progress <= 0:
            print(Fore.RED + "\n💥 Game Over! You lost.")
            break

        try:
            user_guess = int(input("Enter your guess: "))
            if user_guess == 99:
                print("Exiting...")
                break

            if user_guess == number_to_guess:
                print(Fore.GREEN + "Correct!")
                progress += 1
                draw_bar(progress, 'correct')
                number_to_guess = random.randint(1, 10)  # تغییر عدد پس از حدس درست
            else:
                print(Fore.RED + f"Wrong! The number was {number_to_guess}")
                progress -= 1
                draw_bar(progress, 'wrong')

                # درخواست کمک اگر حدس غلط بود
                print("Press Ctrl+Y for a hint.")
                if keyboard.is_pressed('ctrl+y'):  # اگر کلید Ctrl + Y فشرده شد
                    give_hint()
                    help_used += 1  # شمارش کمک‌های استفاده‌شده

            time.sleep(1.5)
        except ValueError:
            print("Please enter a valid number!")
            time.sleep(1)

if __name__ == "__main__":
    play()
