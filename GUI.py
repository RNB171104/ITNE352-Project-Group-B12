import socket
import json
import ssl
import tkinter as tk
from tkinter import messagebox

# Client configuration
HOST = 'localhost'
PORT = 65432

class NewsClientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("News Client")
        self.geometry("600x400")
        self.configure(bg='#FF4081')  # Set background color to dark pink

        self.client_name = ""
        self.group_id = ""
        self.option = ""
        self.query = ""

        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg='#FF4081')  # Set background color to dark pink
        header_frame.pack(pady=10)

        title_label = tk.Label(header_frame, text="News Client", font=("Arial", 20, "bold"), bg='#FF4081', fg='white')  # Set background color to dark pink, text color to white
        title_label.pack(side=tk.LEFT)

        # Form
        form_frame = tk.Frame(self, bg='#FF4081')  # Set background color to dark pink
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Client Name:", font=("Arial", 12), bg='#FF4081', fg='white').grid(row=0, column=0, padx=10, pady=5, sticky="e")  # Set background color to dark pink, text color to white
        self.client_name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.client_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Group ID:", font=("Arial", 12), bg='#FF4081', fg='white').grid(row=1, column=0, padx=10, pady=5, sticky="e")  # Set background color to dark pink, text color to white
        self.group_id_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.group_id_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Option:", font=("Arial", 12), bg='#FF4081', fg='white').grid(row=2, column=0, padx=10, pady=5, sticky="e")  # Set background color to dark pink, text color to white
        self.option_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.option_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Query (if option is 'everything'):", font=("Arial", 12), bg='#FF4081', fg='white').grid(row=3, column=0, padx=10, pady=5, sticky="e")  # Set background color to dark pink, text color to white
        self.query_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.query_entry.grid(row=3, column=1, padx=10, pady=5)

        self.fetch_button = tk.Button(form_frame, text="Fetch News", font=("Arial", 12, "bold"), bg="#F06292", fg="white", command=self.fetch_news)  # Set background color to a brighter shade of pink, text color to white
        self.fetch_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Results
        results_frame = tk.Frame(self, bg='#FF4081')  # Set background color to dark pink
        results_frame.pack(pady=20)

        self.result_label = tk.Label(results_frame, text="", font=("Arial", 12), justify=tk.LEFT, bg='#FF4081', fg='white')  # Set background color to dark pink, text color to white
        self.result_label.pack(padx=20, pady=10)

    def fetch_news(self):
        self.client_name = self.client_name_entry.get()
        self.group_id = self.group_id_entry.get()
        self.option = self.option_entry.get()
        self.query = self.query_entry.get()

        if not self.client_name or not self.group_id or not self.option:
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return

        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations('server.crt')

        try:
            with socket.create_connection((HOST, PORT)) as sock:
                with context.wrap_socket(sock, server_hostname=HOST) as client_socket:
                    client_info = {
                        "client_name": self.client_name,
                        "group_id": self.group_id
                    }
                    client_socket.sendall(json.dumps(client_info).encode('utf-8'))

                    request_data = {
                        "option": self.option,
                        "query": self.query
                    }
                    client_socket.sendall(json.dumps(request_data).encode('utf-8'))

                    response_size = int(client_socket.recv(10).strip())
                    response_message = client_socket.recv(response_size).decode('utf-8')
                    results = json.loads(response_message)

                    # Display the results
                    formatted_results = ""
                    for result in results:
                        formatted_results += f"{result}\n"
                    self.result_label.config(text=formatted_results, fg='white')  # Set text color to white

        except ConnectionRefusedError:
            messagebox.showerror("Error", "Connection refused, please ensure the server is running.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = NewsClientApp()
    app.mainloop()