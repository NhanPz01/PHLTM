import socket
import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import glob

def run_app():
  subprocess.run(['python', 'app.py'])

def send_file(file_path, client_socket):
  with open(file_path, 'rb') as file:
    for data in file:
      client_socket.sendall(data)
  # Send termination signal
  client_socket.sendall(b'FILE_END')

def start_client():
  files = glob.glob('data/*')
  for f in files:
    os.remove(f)
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(('localhost', 12345))

  root = tk.Tk()
  root.title("Chương trình chia danh sách coi thi")
  root.geometry("800x500")

  # Center the window
  window_width = root.winfo_reqwidth()
  window_height = root.winfo_reqheight()
  position_top = int(root.winfo_screenheight() / 2 - window_height / 2 - 250)
  position_right = int(root.winfo_screenwidth() / 2 - window_width / 2 - 400)
  root.geometry("+{}+{}".format(position_right, position_top))

  file_path1 = tk.StringVar()
  file_label1 = tk.Label(root, textvariable=file_path1, font=('Arial', 10))
  file_label1.pack(padx=10, pady=10)  # Add padding

  file_path2 = tk.StringVar()
  file_label2 = tk.Label(root, textvariable=file_path2, font=('Arial', 10))
  file_label2.pack(padx=10, pady=10)  # Add padding

  def choose_file(file_path, file_label):
    file_path.set(filedialog.askopenfilename())
    file_label.config(text=file_path.get())

  def send_files():
    file_paths = [file_path1.get(), file_path2.get()]
    try:
      for file_path in file_paths:
        filename = os.path.basename(file_path)
        client_socket.send(filename.encode('utf-8'))
        send_file(file_path, client_socket)

      # Wait for server's response
      client_socket.settimeout(5.0)  # Set timeout to 5 seconds
      while True:
        try:
          data = client_socket.recv(1024)
          if data == b'ALL_FILES_RECEIVED':
            print("All files have been received by the server.")
            break
        except socket.timeout:
          print("Timeout while waiting for server's response.")
          break
    except Exception as e:
      print(f"An error occurred: {e}")

  choose_button1 = tk.Button(root, text="Chọn file danh sách cán bộ coi thi", command=lambda: choose_file(file_path1, file_label1), font=('Arial', 14), background='SystemButtonFace', highlightbackground='lightgrey')
  choose_button1.pack(padx=10, pady=10)  # Add padding

  choose_button2 = tk.Button(root, text="Chọn file danh sách phòng thi", command=lambda: choose_file(file_path2, file_label2), font=('Arial', 14), background='SystemButtonFace', highlightbackground='lightgrey')
  choose_button2.pack(padx=10, pady=10)  # Add padding

  send_button = tk.Button(root, text="Gửi file", command=send_files, font=('Arial', 14), background='SystemButtonFace', highlightbackground='lightgrey')
  send_button.pack(padx=10, pady=10)  # Add padding
  
  run_app_button = tk.Button(root, text="Chia phòng", command=run_app, font=('Arial', 14), background='SystemButtonFace', highlightbackground='lightgrey')
  run_app_button.pack(padx=10, pady=10)  # Add padding

  root.mainloop()

  client_socket.close()

if __name__ == "__main__":
  start_client()