import random as r
from colorama import init , Fore ,Style , Back



init()


def start():
    print("Number-guessing-game")
    print('''Hello, welcome to the number guessing game 
Are you ready [yes or no]?''')
def inputy():
    entered_number=input()
    return str(entered_number)


    
def Number_generator():
    number=r.randint(0,10)
    while(True):
        y=int(input("A number between 1 and 10 :\t "))
        
        if y==number:
            print(f"That was great, you guessed the number correctly:{number}")

            break
        elif number<y:
            print(f"of this{y} is smaller")
        elif number>y:
            print(f"of this{y} is bigger")
        if y==99:
            ready(y)
            break

def ready (x):
    if (str(x)=="1"or str(x).lower in ["y","yes","ye"] ):
       Number_generator()
    elif str(x)=="0" or str(x).lower in ["no" , "n" , "0"]:
        print("nooo goodbye")
    if x in [99 , "99" , "exit"] :
        exit()
     


if __name__=="__main__":
    # print(Fore.BLUE,f"{"hi"}")
    start()
    ready(inputy())

    
    

    