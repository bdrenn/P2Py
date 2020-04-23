from src.node import Node 


# Main loop 

def menu():
    response = int(input("Please choose an option: "))
    return response


while True:

    choice = menu()

    if choice == 1:
        print("I am choice 1")
        pass

    if choice == 5: 
        break