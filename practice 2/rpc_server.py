from xmlrpc.server import SimpleXMLRPCServer
import os

HOST = "localhost"
PORT = 8000
STORAGE = "./server_files"

# Create storage folder
if not os.path.exists(STORAGE):
    os.makedirs(STORAGE)

def upload_file(filename, binary_data):
    """Receive file from client"""
    try:
        filepath = os.path.join(STORAGE, filename)
        with open(filepath, "wb") as handle:
            handle.write(binary_data.data)
        print(f"Received: {filename}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def download_file(filename):
    """Send file to client"""
    try:
        filepath = os.path.join(STORAGE, filename)
        if not os.path.exists(filepath):
            return None
        with open(filepath, "rb") as handle:
            from xmlrpc.client import Binary
            return Binary(handle.read())
    except Exception as e:
        print(f"Error: {e}")
        return None

def list_files():
    """List all files"""
    try:
        files = os.listdir(STORAGE)
        return [f for f in files if os.path.isfile(os.path.join(STORAGE, f))]
    except:
        return []

if __name__ == "__main__":
    server = SimpleXMLRPCServer((HOST, PORT))
    
    server.register_function(upload_file)
    server.register_function(download_file)
    server.register_function(list_files)
    
    print(f"RPC Server running at http://{HOST}:{PORT}/")
    print("Press Ctrl+C to stop")
    
    server.serve_forever()
