import socket
import os
import threading

def handle_client(client_socket):
  while True:
    # Receive the file name
    file_name = client_socket.recv(1024).decode('utf-8')
    if not file_name:
      # No more files to receive
      break

    with open(os.path.join('data', file_name), 'wb') as file:
      print("đang nhận file: " + file_name)
      while True:
        data = client_socket.recv(1024)
        if data == b'FILE_END':
          # End of file
          break
        file.write(data)
      print("đã nhận thành công: " + file_name)

  # Send response back to the client
  client_socket.sendall(b'ALL_FILES_RECEIVED')

def start_server():
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind(('localhost', 12345))
  server_socket.listen(5)

  print("Server is listening on port 12345...")

  while True:
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()

if __name__ == "__main__":
  start_server()