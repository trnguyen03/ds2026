#!/usr/bin/env python3
"""
MPI File Transfer
Run: mpiexec -n 2 python3 mpi_file_transfer.py [file_path]
"""

from mpi4py import MPI
import os
import sys

CHUNK_SIZE = 1024

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Get file path from argument or use default
file_path = sys.argv[1] if len(sys.argv) > 1 else "file.txt"

if rank == 0:
    # === SENDER (Rank 0) ===
    if not os.path.exists(file_path):
        # Create test file if not exists
        with open(file_path, "w") as f:
            f.write("Hello from MPI!\nThis is a test file.\n")
    
    filename = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)
    
    print(f"[Rank 0] Sending: {filename} ({filesize} bytes)")
    
    # Send metadata
    comm.send(filename, dest=1, tag=0)
    comm.send(filesize, dest=1, tag=1)
    
    # Send file chunks
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            comm.send(chunk, dest=1, tag=2)
    
    print(f"[Rank 0] File sent successfully!")

else:
    # === RECEIVER (Rank 1) ===
    filename = comm.recv(source=0, tag=0)
    filesize = comm.recv(source=0, tag=1)
    
    print(f"[Rank 1] Receiving: {filename} ({filesize} bytes)")
    
    # Receive and write chunks
    with open("received_" + filename, "wb") as f:
        received = 0
        while received < filesize:
            chunk = comm.recv(source=0, tag=2)
            f.write(chunk)
            received += len(chunk)
    
    print(f"[Rank 1] File saved as: received_{filename}")

# Sync
comm.Barrier()

if rank == 0:
    print("Done!")
