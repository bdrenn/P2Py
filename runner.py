from src.node import Node
import argparse


app_name = """
 _____ _             ____                
|_   _(_)_ __  _   _|  _ \ ___  ___ _ __ 
  | | | | '_ \| | | | |_) / _ \/ _ \ '__|
  | | | | | | | |_| |  __/  __/  __/ |   
  |_| |_|_| |_|\__, |_|   \___|\___|_|          """
# Main loop :)
def print_menu():
    print(app_name, "\n")
    print("1. Get Peers")
    print("2. Set File")
    print("3. Get File")
    print("4. Edit File")
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
            print("Getting Peers...")
            print(node.get_peers())
        elif choice==2:
            file_name = input('Enter the file name: ')
            #file_value = input('Enter file value: ')
            file_value = open(file_name, "r")
            node.set_file(file_name, file_value.read())
            print('File set!')
            file_value.close()
        elif choice==3:
            file_name = input('Enter the file name: ')
            file_value = node.get_file(file_name)
            file = open(file_name, "w")
            file.write(file_value)
            print('File: ', file_value)
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