import socket
import os
import struct
import sys

HOST = '127.0.0.1'
PORT = 8080

def send_file(filepath):
    if not os.path.exists(filepath):
        print("File not found.")
        return

    file_size = os.path.getsize(filepath)
    filename = os.path.basename(filepath).encode('utf-8')
    name_len = len(filename)

    print(f"Sending: {filepath} ({file_size / (1024*1024):.2f} MB)")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            
            header = struct.pack(f'!IQ{name_len}s', name_len, file_size, filename)
            s.sendall(header)

            with open(filepath, 'rb') as f:

                sent = s.sendfile(f)
            
            if sent == file_size:
                print(f"Success! Sent {sent} bytes via Zero-Copy.")
            else:
                print(f"Warning: Only sent {sent}/{file_size} bytes.")

    except ConnectionRefusedError:
        print("Server connection failed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <file_path>")
    else:
        send_file(sys.argv[1])