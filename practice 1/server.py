import socket
import os
import struct

HOST = '0.0.0.0' 
PORT = 8080
BUFFER_SIZE = 65536 

def receive_all(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            print(f"\nConnected: {addr}")
            
            try:
                fixed_header = receive_all(conn, 12)
                if not fixed_header:
                    continue
                
                name_len, file_size = struct.unpack('!IQ', fixed_header)

                filename_bytes = receive_all(conn, name_len)
                filename = filename_bytes.decode('utf-8')
                
                safe_filename = f"RECV_{os.path.basename(filename)}"
                print(f"Downloading: {safe_filename} ({file_size / (1024*1024):.2f} MB)")

                received = 0
                with open(safe_filename, 'wb') as f:
                    while received < file_size:
                        to_read = min(BUFFER_SIZE, file_size - received)
                        chunk = conn.recv(to_read)
                        if not chunk: break
                        f.write(chunk)
                        received += len(chunk)
                
                print("Transfer complete.")
                
            except Exception as e:
                print(f"Error: {e}")
            finally:
                conn.close()
                
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server_socket.close()

if __name__ == '__main__':
    start_server()