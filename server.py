import socket
import threading
import requests
import json
import errno
from time import sleep

# Server socket address.
HOST_ADDRESS = '127.0.0.1'
HOST_PORT = 49999

# Defining our constants.
MAIN_MENU = "Main Menu:\n1- Search Headlines\n2- List of Sources\n3- Quit\n"
HEADLINES_MENU = "Headlines Menu:\n1- Search for Keywords\n2- Search by Category\n3- Search by Country\n4- List All News Headlines\n5- Back to the Main Menu\n"
SOURCES_MENU = "Sources Menu:\n1- Search by Category\n2- Search by Country\n3- Search by Language\n4- List All Sources\n5- Back to the Main Menu\n"
API_KEY = "d0fd49c4febf410f8cbafe832fdb9eba"


# So that we only have 15 responses.
parameters = {
     'limit': '15'
}


# To handle user country choices.
def country_parameters(country):
    if country == "1":
        return "au"
    elif country == "2":
        return "nz"
    elif country == "3":
        return "ca"
    elif country == "4":
        return "ae"
    elif country == "5":
        return "sa"
    elif country == "6":
        return "gb"
    elif country == "7":
        return "us"
    elif country == "8":
        return "eg"
    elif country == "9":
        return "ma"


# To handle user category choices.
def category_parameters(category):
    if category == "1":
        return "business"
    elif category == "2":
        return "entertainment"
    elif category == "3":
        return "general"
    elif category == "4":
        return "health"
    elif category == "5":
        return "science"
    elif category == "6":
        return "sports"
    elif category == "7":
        return "technology"


# To handle user language choices.
def language_parameters(language):
    if language == "1":
        return "english"
    elif language == "2":
        return "arabic"
    

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
def handle_TheHeadline_menu(request, client_socket, client_address):

    file_name = f"GroupA5_{client_address[1]}HeadlineRequest{request}.json"
    string = request.split(".")
    while True:
        
        if string[0] == "1":
            url = f"https://newsapi.org/v2/top-headlines?q={string[1]}&apiKey={API_KEY}"    
        elif string[0] == "2":
            url = f"https://newsapi.org/v2/top-headlines?category={category_parameters(string[1])}&apiKey={API_KEY}"
        elif string[0] == "3":
            url = f"https://newsapi.org/v2/top-headlines?country={country_parameters(string[1])}&apiKey={API_KEY}"
        elif string[0] == "4":
            url = f"https://newsapi.org/v2/top-headlines?apiKey={API_KEY}"
        elif string[0] == "5":
            client_socket.sendall(MAIN_MENU.encode())
            break
        else:
            client_socket.sendall("Invalid option. Please try again.".encode())

        response = requests.get(url, params=parameters)
        if response.status_code == 200:
            # To add the fetched data in a json file.
            with open( file_name , 'w') as file:
                json.dump(response.json(), file, indent= 2)
            # To put the fetched data in a list.
            data =response.json() 
            articles = data["articles"]

            # Display summarized list of news headlines
            if len(articles) > 0:
                summary_list = [
                    f"Source: {articles['source']['name']}\nAuthor: {articles['author']}\nTitle: {articles['title']}\n"
                    for articles in articles    
                ]
            summary_response = "\n".join(summary_list)
            client_socket.sendall(summary_response.encode())
            sleep(2)
            # Get user choice of headline to see more information about.
            option_index = client_socket.recv(1024).decode().strip()
            chosen_headline = articles[int(option_index)]    
            if int(option_index) < 0 or int(option_index) >= len(articles):
                article_details = {
                    "Source": chosen_headline['source']['name'],
                    "Author": chosen_headline['author'],
                    "Title": chosen_headline['title'],     
                    "URL": chosen_headline['url'],
                    "Description": chosen_headline['description'],
                    "Publish Date": chosen_headline['publishedAt'].split("T")[0],
                    "Publish Time": chosen_headline['publishedAt'].split("T")[1].split("Z")[0]
                }
                details_response = json.dumps(article_details, indent=2)
                client_socket.sendall(details_response.encode())
                break
            else:
                client_socket.sendall(b"Invalid option. Please try again.").encode()   
        else:
            raise requests.exceptions.RequestException(f"GET {url} {response.status_code} {response.reason}")
        

# Handling sources sub-menu.
def handle_TheSource_menu(request, client_socket, client_address):

    file_name = f"GroupB12_{client_address[1]}_{request}.json"
    string = request.split(".")

    while True:
        if string[0] == '1':
            url = f"https://newsapi.org/v2/sources?category={category_parameters(string[1])}&apiKey={API_KEY}"
        elif string[0] == '2':
            url = f"https://newsapi.org/v2/sources?country={country_parameters(string[1])}&apiKey={API_KEY}"
        elif string[0] == '3':
            url = f"https://newsapi.org/v2/sources?language={language_parameters(string[1])}&apiKey={API_KEY}"
        elif string[0] == "4":
            url = f"https://newsapi.org/v2/sources?apiKey={API_KEY}"
        elif string[0] == "5":
            client_socket.sendall(MAIN_MENU.encode())
            break
        else:
            client_socket.sendall("Invalid option. Please try again.".encode())

        response = requests.get(url, params=parameters)
        if response.status_code == 200:
            # To add the fetched data in a json file.
            with open( file_name , 'w') as file:
                json.dump(response.json(), file, indent= 2)
            # To put the fetched data in a list.
            data = response.json()
            sources = data["sources"]

            # Display list of the fetched request sources
            if len(sources) > 0:
                source_response = "\n".join([f"{index + 1}. {source['name']}" for index, source in enumerate(sources)])
            client_socket.sendall(source_response.encode())
            sleep(2)

            # Get user choie of source to see more information about.
            option_index = client_socket.recv(1024).decode().strip()
            chosen_source = sources[int(option_index)]    
            if int(option_index) < 0 or int(option_index) >= len(sources):    
                chosen_source = sources[option_index]
                source_details = {
                    f"Source: {chosen_source['name']}",
                    f"Country: {chosen_source['country']}",
                    f"Description: {chosen_source['description']}",
                    f"URL: {chosen_source['url']}",
                    f"Category: {chosen_source['category']}",
                    f"Language: {chosen_source['language']}"
                }
                source_details_response = "\n".join(source_details)
                client_socket.sendall(source_details_response.encode())
                break
            else:
                client_socket.sendall(b"Invalid choice please try again.")
        else:
            raise requests.exceptions.RequestException(f"GET {url} {response.status_code} {response.reason}")
    

# Function to handle every client connection.
def handle_clients_connections(client_socket, client_address):

    # Displaying the connected client information.
    print("Connection accepted from ", client_address[0], " with port number ", client_address[1])

    # Sending the main menu to the client
    client_socket.send(MAIN_MENU.encode())

    while True:
        try:
            # Receiving client request.
            main_menu_request = client_socket.recv(1024).decode().strip()

            # Handling sub-menu request and response.
            if main_menu_request == '1':
                while True:
                    client_socket.sendall(handle_main_menu_request(main_menu_request).encode())
                    sub_menu_request = client_socket.recv(1024).decode().strip()
                    handle_TheHeadline_menu(sub_menu_request, client_socket, client_address)
                    if sub_menu_request == "5":
                        break

            elif main_menu_request == '2':
                while True:
                    client_socket.sendall(handle_main_menu_request(main_menu_request).encode())
                    sub_menu_request = client_socket.recv(1024).decode().strip()
                    handle_TheSource_menu(sub_menu_request, client_socket, client_address)
                    if sub_menu_request == "5":
                        break

            # Display goodbye message and stop program.
            elif main_menu_request == '3':
                client_socket.sendall(handle_main_menu_request(main_menu_request).encode())
                # Closing client connection.
                print("Client", client_address[0], "with port number", client_address[1], "disconnected.")
                break

        except socket.error as e:
            if e.errno == errno.ECONNRESET:
                # Handle connection reset error
                print(f"Connection was ended unexpectdly by peer with port number {client_address[1]}")
                break
            else:
                # Handle other socket errors
                print("Socket error occurred:", e)
                break

    client_socket.close()       
                

# Creating a TCP socket and listening to client connections.
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket: 

    server_socket.bind((HOST_ADDRESS, HOST_PORT))
    server_socket.listen(5)
    print("Server is listening ..")

    # Loop to handle multiple connections.
    while True:

        # Accepting multiple client connections.
        client_socket, client_add = server_socket.accept()
        client_thread = threading.Thread(target= handle_clients_connections, args=(client_socket, client_add))
        client_thread.start()