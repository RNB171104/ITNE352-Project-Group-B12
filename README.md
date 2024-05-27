# News Site With Client-Server TCP Connection

## Project description 
In order to exchange requests and responses based on the news or information that the clients require, we designed server-client scripts for this project. We also added API, multithreading, and a graphical user interface. Multiple clients can be handled by the server script.

## Our information
Semester: 2023/2024
Course Code: ITNE352 
Section: 2
Group: B12


### Students
Sara Hamad Darwish Alshaiji-202109954
Reem Nayef Buasali-202202875

## Table of content
1. Requirements
2. How to run files 
3. Scripts explanation   
4. Additional concepts 
5. Acknowledgments 
6. Conclusion


## Requirments:
1. **Python** you should install it to work on your project and run your code you either install it by 
 [pycharm]:(https://www.jetbrains.com/pycharm/download/?section=mac) -pycharm installation
 or
 [visualstudiocode]:(https://code.visualstudio.com/download)- vs code installation

2. **News API Key** to have your key
 [APIKey]:(https://newsapi.org)-Api key

3. **Module** to perform Http request you need the , to download it go to your terminal and type this command `python -m pip install requests`


## How to run the system
1. save the client and server files on your PC
2. Run the server file `Server.py` , by typing in the your terminal the following command :`python Server.py`
3. Run the client file `Client.py` ,by typing in the your terminal the following command :`python Client.py` ,if you will run multipule clients just open multiple terminal windows
4. Now you can start asking for the option that you need in the menu that will be shown after runing both files then the server will respond with the nedded information

## Brief describtion of the script:
### 1.Client script------------------------------------------------------------------------------------------------
#### -import statments needed:

```python
import socket
from time import sleep
```
**import socket**: allowing you to create, connect, and communicate with sockets.
**from time import sleep**: allows you to pause the execution of your program for a specified number of seconds.


#### The creation of the client socket
```python

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_ADDRESS, HOST_PORT))
```
This code creates TCP socket for the client and establish connection with the server.

#### -Variables:
```python
#Server socket address
HOST_ADDRESS = '127.0.0.1'
HOST_PORT = 49999
```




#### Client function 
```python
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

```
This meanu display the option based on what the client choose and display the respond

### 2.Server sciprt------------------------------------------------------------------------------------------------
#### -import statments needed:
```python
import socket
import threading
import requests
import json
import errno
from time import sleep
```
**import socket**: allowing you to create, connect, and communicate with sockets.
**import threading**: provides support for spawning multiple threads of execution within a single process.
**import requests**:making HTTP requests.
**import json**: functions for encoding and decoding JSON data.
**import errno**: provides access to the error codes.
**from time import sleep**: allows you to pause the execution of your program for a specified number of seconds.

#### -The creation of the client socket
```python

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket: 

    server_socket.bind((HOST_ADDRESS, HOST_PORT))
    server_socket.listen(5)
    print("Server is listening ..")

Creating a TCP socket and listening to client connections.
```

#### -Variables:

```python
#Server socket address
HOST_ADDRESS = '127.0.0.1'
HOST_PORT = 49999
#Constant
MAIN_MENU = "Main Menu:\n1- Search Headlines\n2- List of Sources\n3- Quit\n"
HEADLINES_MENU = "Headlines Menu:\n1- Search for Keywords\n2- Search by Category\n3- Search by Country\n4- List All News Headlines\n5- Back to the Main Menu\n"
SOURCES_MENU = "Sources Menu:\n1- Search by Category\n2- Search by Country\n3- Search by Language\n4- List All Sources\n5- Back to the Main Menu\n"
API_KEY = "d0fd49c4febf410f8cbafe832fdb9eba"
```

The previous variables are the address of the server socket and the menu that will be shown to the client when they choose.

#### -Number of requests:
```python
parameters =
{
     'limit': '15'
}
```
This means that they server can handle up to 15 requests.

#### -Server functiones

1. 
```python
#This function handles the main menu request ,it will apper as the first mean optiones
def handle_main_menu_request(request):
    if request == '1':
        return HEADLINES_MENU
    elif request == '2':
        return SOURCES_MENU
    elif request == '3':
        return "Thank you for using our server. Goodbye!\n"
    else:
        return "Invalid option selection. Please try again\n" 
    


# This funcion handle user country choices.
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
    
```    



## Additional concepts
1. **Multithreading**: where we used it to handle multiple threds at the same time
2. **GUI**: its a graphical user interface so it help the client to interact with it.

## Acknowledgments
we are thankful for Dr.Mohammed Almeer for his valuable knowledge that he was glad to share with us and help us during the project .
## Conclusion
This project shows how to gather and display news content using a client-server architecture.  It demonstrates how to integrate APIs, connect to networks, and multithread using Python.

