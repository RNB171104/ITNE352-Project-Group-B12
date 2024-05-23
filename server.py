import socket
import threading

# Server socket address.
HOST_ADDRESS = '127.0.0.1'
HOST_PORT = 49999

# Defining our menus as constants.
MAIN_MENU = "Main Menu:\n1- Search Headlines\n2- List of Sources\n3- Quit\n"
HEADLINES_MENU = "Headlines Menu:\n1- Search for Keywords\n2- Search by Category\n3- Search by Country\n4- List All News Headlines\n5- Back to the Main Menu\n"
SOURCES_MENU = "Sources Menu:\n1- Search by Category\n2- Search by Country\n3- Search by Language\n4- List All Sources\n5- Back to the Main Menu\n"

# Handling the main menu request.
def handle_main_menu_request(request):
    if request == '1':
        return HEADLINES_MENU
    elif request == '2':
        return SOURCES_MENU
    elif request == '3':
        return "Thank you for using our server. Goodbye!\n"
    else:
        return "Invalid option selection. Please try again\n" 

# Handling the headlines sub-menu.    
def handle_headline_menu(request):

    if request == '1':
        return "search by keyword...\n"
    elif request == '2':
        return "search by category...\n"
    elif request == '3':
        return "search by country...\n"
    elif request == '4':
        return "List all news headlines...\n"
    elif request == '5':
        return MAIN_MENU
    else:
        return "Invalid option selection. Please try again.\n"

# Handling sources sub-menu.
def handle_source_menu(request):
    
    if request == '1':
        return "search by category...\n"
    elif request == '2':
        return "search by country...\n"
    elif request == '3':
        return "search by language...\n"
    elif request == '4':
        return "List all sources...\n"
    elif request == '5':
        return MAIN_MENU
    else:
        return "Invalid option selection. Please try again.\n"

# Function to handle every client connection.
def handle_clients_connections(conn, add):
    # Displaying the connected client information.
    print(f"Connection accepted from {add[0]} with port number {add[1]}")

    # Sending the main menu to the client
    conn.send(MAIN_MENU.encode())

    while True:
        # Receiving client request.
        main_menu_request = conn.recv(1024).decode().strip()
        
        # Handling sub-menu request and response.
        if main_menu_request == '1' or main_menu_request == '2':
            while True:
                # To send Appropreate sub-menu and response.
                if main_menu_request == '1':
                    conn.sendall(handle_main_menu_request(main_menu_request).encode())
                    sub_menu_request = conn.recv(1024).decode().strip()
                    response = handle_headline_menu(sub_menu_request)
                elif main_menu_request == '2':
                    conn.sendall(handle_main_menu_request(main_menu_request).encode())
                    sub_menu_request = conn.recv(1024).decode().strip()
                    response = handle_source_menu(sub_menu_request)

                conn.sendall(response.encode())
                if response == MAIN_MENU:
                    break

        # Displaying goodbuy message and stopping program.
        elif main_menu_request == '3':
            conn.send(handle_main_menu_request(main_menu_request).encode())

            # Closing client connection.
            print("Client ", add[0], " with port number ", add[1], "disconnected.")
            break

        # Display invalid input message.
        else:
            conn.send(handle_main_menu_request(main_menu_request).encode())
    conn.close()     
                

# Creating a TCP socket and listening to client connections.
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as ss:  

    ss.bind((HOST_ADDRESS, HOST_PORT))
    ss.listen()
    print("Server is listening ..")

    # Loop to handle multiple connections.
    while True:

        # Accepting multiple client connections.
        conn, add = ss.accept()
        t = threading.Thread(target= handle_clients_connections, args=(conn , add))
        t.start() 
    