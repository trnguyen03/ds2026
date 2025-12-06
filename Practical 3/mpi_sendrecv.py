#!/usr/bin/env python3

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    # Send data to rank 1
    data = {"name": "Nguyen", "id": "22BA13239"}
    comm.send(data, dest=1, tag=11)
    print(f"[Rank 0] Sent: {data}")
    
elif rank == 1:
    # Receive data from rank 0
    data = comm.recv(source=0, tag=11)
    print(f"[Rank 1] Received: {data}")

