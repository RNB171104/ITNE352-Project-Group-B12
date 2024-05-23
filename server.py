import socket

# Server configuration
HOST = 'localhost'
PORT = 4012

# Menus
MAIN_MENU = "Main Menu:\n1. Search Headlines\n2. List of Sources\n3. Quit\n"
HEADLINES_MENU = "Headlines Menu:\n1. Search by Keyword\n2. Search by Category\n3. Search by Country\n4. List All News Headlines\n5. Back to Main Menu\n"
SOURCES_MENU = "Sources Menu:\n1. Search by Category\n2. Search by Country\n3. Search by Language\n4. List All Sources\n5. Back to Main Menu\n"

# Function to handle client requests
def handle_request(request):
    if request == '1':
        return HEADLINES_MENU
    elif request == '2':
        return SOURCES_MENU
    elif request == '3':
        return "Goodbye!\n"
    else:
        return "Invalid choice. Please try again.\n"

# Function to handle sub-menu requests
def handle_submenu_request(request, menu):
    if menu == 'headlines':
        if request == '1':
            return "Performing search by keyword...\n"
        elif request == '2':
            return "Performing search by category...\n"
        elif request == '3':
            return "Performing search by country...\n"
        elif request == '4':
            return "Listing all news headlines...\n"
        elif request == '5':
            return MAIN_MENU
        else:
            return "Invalid choice. Please try again.\n"
    elif menu == 'sources':
        if request == '1':
            return "Performing search by category...\n"
        elif request == '2':
            return "Performing search by country...\n"
        elif request == '3':
            return "Performing search by language...\n"
        elif request == '4':
            return "Listing all sources...\n"
        elif request == '5':
            return MAIN_MENU
        else:
            return "Invalid choice. Please try again.\n"

# Create TCP socket and listen for client connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Server started and listening for connections...")

    while True:
        # Accept client connection
        client_socket, client_address = server_socket.accept()
        print(f"Client connected: {client_address}")

        # Send main menu to client
        client_socket.sendall(MAIN_MENU.encode())

        while True:
            # Receive client request
            request = client_socket.recv(1024).decode().strip()

            # Handle client request and send response
            if request == '3':
                client_socket.sendall(handle_request(request).encode())
                break
            elif request == '1' or request == '2':
                client_socket.sendall(handle_request(request).encode())
                menu = 'headlines' if request == '1' else 'sources'
                while True:
                    submenu_request = client_socket.recv(1024).decode().strip()
                    response = handle_submenu_request(submenu_request, menu)
                    client_socket.sendall(response.encode())
                    if response == MAIN_MENU:
                        break
            else:
                client_socket.sendall(handle_request(request).encode())

        # Close client connection
        client_socket.close()
        print(f"Client disconnected: {client_address}")