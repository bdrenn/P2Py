from src.node import Node
import asyncio

host_port = 1001
user_port = 1002
host_IP = '0.0.0.0'

async def setup_node():
    node = Node()

    try:
        print("hello")
        await node.listening(host_port)
        print("First node ")
    except Exception as e:
        try:
            await node.listening(int(user_port))
            await node.join_network_node(host_IP, host_port)
        except Exception as e:
            print(e)

    peers = await node.get_peers()
    print(peers)

    return node






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

async def main():
    node = await setup_node()
    while True:
        print_menu() 
        choice = int(input("Enter your choice [1-5]: "))

        await node.listening(user_port)
        
        if choice==1:     
            print("Getting peers...")
            print(await node.get_peers())
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

asyncio.run(main())