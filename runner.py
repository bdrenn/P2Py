from src.node import Node
import argparse
import json
import ntpath

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
            file_path = input('Enter the path to the file: ')
            file_name = ntpath.basename(file_path)
            #file_value = input('Enter file value: ')
            file_value = open(file_path, "r")
            json_dump = json.dumps(file_value.read())
            node.set_file(file_name, json_dump)
            print('File set!')
            file_value.close()
        elif choice==3:
            file_name = input('Enter the file name: ')
            json_value = node.get_file(file_name)
            file_value = json.loads(json_value)
            file = open('storage/' + file_name, "w")
            file.write(file_value)
            print('File: ', file_value)
            file.close()
        elif choice==4:
            file_name = input("Enter the file name you want to edit: ")
            file = open('storage/' + file_name, "w")
            print("File succesfully opened")
            file_edit = input("Enter the edits to the file: ")
            file.write(file_edit)
            print("File succesfully edited")
            file.close() 
        elif choice==5:
            print("Thanks for joining us!")
            ## need a way of stopping all threads and exiting program
            ## You can add your code or functions here
            break
        else:
            choice = input("Wrong option selection. Enter any key to try again..")


my_parser = argparse.ArgumentParser(description= 'File sharing application')

my_parser.add_argument('--verbose', action='store_true', help='Display logs' )
args = my_parser.parse_args()

main(args)