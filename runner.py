from src.node import Node
import argparse


app_name = """
 _____ _             ____                
|_   _(_)_ __  _   _|  _ \ ___  ___ _ __ 
  | | | | '_ \| | | | |_) / _ \/ _ \ '__|
  | | | | | | | |_| |  __/  __/  __/ |   
  |_| |_|_| |_|\__, |_|   \___|\___|_|          """
# Main loop 
def print_menu():
    print(app_name, "\n")
    print("1. Menu Option 1")
    print("2. Menu Option 2")
    print("3. Menu Option 3")
    print("4. Menu Option 4")
    print("5. Exit")

def main(args):
    node = Node()

    if args.verbose is True:
        node.log()

    node.setup()
    
    while True:
        print_menu() 
        choice = int(input("Enter your choice [1-5]: "))
        
        if choice==1:     
            print("Getting peers...")
            print(node.get_peers())
        elif choice==2:
            print("Menu 2 has been selected")
            ## You can add your code or functions here
        elif choice==3:
            print("Menu 3 has been selected")
            ## You can add your code or functions here
        elif choice==4:
            print("Menu 4 has been selected")
            ## You can add your code or functions here
        elif choice==5:
            print("Menu 5 has been selected")
            ## You can add your code or functions here
            break
        else:
            choice = input("Wrong option selection. Enter any key to try again..")


my_parser = argparse.ArgumentParser(description= 'File sharing application')

my_parser.add_argument('--verbose', action='store_true', help='Display logs' )
args = my_parser.parse_args()

main(args)