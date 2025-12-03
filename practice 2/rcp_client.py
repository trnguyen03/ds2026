import xmlrpc.client
import os

SERVER_URL = "http://localhost:8000/"

def send_file(filename):
    if not os.path.exists(filename):
        print("File does not exist!")
        return

    print(f"Connecting to {SERVER_URL}...")
    
    proxy = xmlrpc.client.ServerProxy(SERVER_URL)

    try:
        with open(filename, "rb") as handle:
            binary_data = xmlrpc.client.Binary(handle.read())
            
            print(f"Calling remote function 'upload_file' to send {filename}...")
            
            result = proxy.upload_file(os.path.basename(filename), binary_data)
            
            if result:
                print("File sent successfully!")
            else:
                print("File send failed (Server error).")
                
    except ConnectionRefusedError:
        print("Could not connect. Please ensure Server is running.")
    except Exception as e:
        print(f"Error: {e}")

def receive_file(filename):
    print(f"Connecting to {SERVER_URL}...")
    
    proxy = xmlrpc.client.ServerProxy(SERVER_URL)

    try:
        print(f"Calling remote function 'download_file' to get {filename}...")
        
        result = proxy.download_file(filename)
        
        if result:
            with open(filename, "wb") as handle:
                handle.write(result.data)
            print(f"File received successfully! Saved as {filename}")
        else:
            print("File not found on server.")
                
    except ConnectionRefusedError:
        print("Could not connect. Please ensure Server is running.")
    except Exception as e:
        print(f"Error: {e}")

def list_files():
    print(f"Connecting to {SERVER_URL}...")
    
    proxy = xmlrpc.client.ServerProxy(SERVER_URL)

    try:
        files = proxy.list_files()
        
        if files:
            print("\nFiles on server:")
            for f in files:
                print(f"  - {f}")
        else:
            print("No files on server.")
                
    except ConnectionRefusedError:
        print("Could not connect. Please ensure Server is running.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("1. Send file")
    print("2. Receive file")
    print("3. List files")
    
    choice = input("Choose option: ")
    
    if choice == "1":
        fname = input("Enter filename to send: ")
        send_file(fname)
    elif choice == "2":
        fname = input("Enter filename to receive: ")
        receive_file(fname)
    elif choice == "3":
        list_files()
    else:
        print("Invalid option")
