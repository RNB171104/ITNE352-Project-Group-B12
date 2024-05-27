import socket
from time import sleep

# Server socket address.
HOST_ADDRESS = '127.0.0.1'
HOST_PORT = 49999

# Creating a TCP socket and connecting to the server.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_ADDRESS, HOST_PORT))

# Receiving the main menu from the server.
main_menu = client_socket.recv(1024).decode()

while True:
    # Displaying the main menu.
    print(main_menu)

    # Get user option for the main menu.
    main_menu_option = input("Enter your desired option: ")

    # Sending the main menu request to the server.
    client_socket.sendall(main_menu_option.encode())

    if main_menu_option == '1': 
        # Receiving and displaying the chosen sub-menu.
        sub_menu = client_socket.recv(1024).decode()
        while True:
            
            print(sub_menu)

            # Get user option for sub-menu.
            sub_menu_option = input("Please enter your desired option: ")

            # Check if the user wants to go back to the main menu.
            if sub_menu_option == '5':
            # Send command to go back to the main menu.
                msg = "5."
                client_socket.sendall(msg.encode())
                break

            # Get user specific input for search.
            if sub_menu_option == '1':
                keyword = input("Please enter the keyword: ")
                msg = "1."+keyword
            elif sub_menu_option == '2':
                print("Choose the category you want:\n1- business\n2- entertainment\n3- general\n4- health\n5- science\n6- sports\n7- technology.\n")
                category = input("Enter your desired option:")
                msg = "2."+category
            elif sub_menu_option == '3':
                print("Choose the country you want:\n1- Australia\n2- New Zealand\n3- Canada\n4- United Arab Emirates\n5- Saudi Arabia\n6- United Kingdom\n7- United States\n8- Egypt\n9- Morocco\n")
                country = input("Enter your desired option: ")
                msg = "3."+country
            elif sub_menu_option == '4':
                msg = "4."
            else:
                print("Invalid option. Please try again.")
                #continue

            # Send user input to search to the server.
            client_socket.sendall(msg.encode())

            # Receive and display sub-menu response.
            sub_menu_response = client_socket.recv(1024).decode()
            if sub_menu_response == "Main Menu:\n1- Search Headlines\n2- List of Sources\n3- Quit\n":
                break
            else:
                print(sub_menu_response,"\n")
                sleep(2)
                details_option = input("Enter the headline number that you want to read more about: ")
                client_socket.sendall(details_option.encode())
                details = client_socket.recv(1024).decode()
                print(details)

    elif main_menu_option == '2':
        # Receiving and displaying the chosen sub-menu.
        sub_menu = client_socket.recv(1024).decode()
        while True:
            
            print(sub_menu)

            # Get user option for sub-menu.
            sub_menu_option = input("Please enter your desired option: ")

            # Check if the user wants to go back to the main menu.
            if sub_menu_option == '5':
            # Send command to go back to the main menu.
                msg = "5."
                client_socket.sendall(msg.encode())
                break

            # Get user specific input for search.
            if sub_menu_option == '1':
                print("Choose the category you want:\n1- business\n2- entertainment\n3- general\n4- health\n5- science\n6- sports\n7- technology.\n")
                category = input("Choose your desired option:")
                msg = "1."+category
            elif sub_menu_option == '2':
                print("Choose the country you want:\n1- Australia\n2- New Zealand\n3- Canada\n4- United Arab Emirates\n5- Saudi Arabia\n6- United Kingdom\n7- United States\n8- Egypt\n9- Morocco\n")
                country = input("Enter your desired option: ")
                msg = "2."+country
            elif sub_menu_option == '3':
                print("Choose your language:\n1- English\n2- Arabic\n")
                language = input("Enter your desired option: ")
                msg = "3."+language
            elif sub_menu_option == '4':
                msg = "4."
            else:
                print("Invalid option. Please try again.")
                continue

            # Send user input to search to the server.
            client_socket.sendall(msg.encode())

            # Receive and display sub-menu response.
            sub_menu_response = client_socket.recv(1024).decode()
            if sub_menu_response == "Main Menu:\n1- Search Headlines\n2- List of Sources\n3- Quit\n":
                break
            else:
                print(sub_menu_response,"\n")
                sleep(2)
                details_option = input("Enter the source that you want to read more about: ")
                client_socket.sendall(details_option.encode())
                details = client_socket.recv(1024).decode()
                print(details)


    elif main_menu_option == '3':
        # Print goodbye message and break the loop to stop the program.
        response = client_socket.recv(1024).decode()
        print(response,"\n")
        break

    else:
        # Receive and print the output of an invalid option.
        response = client_socket.recv(1024).decode()
        print(response,"\n")

# Closing the client socket.
client_socket.close()