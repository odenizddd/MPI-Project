#!/usr/bin/env python
from mpi4py import MPI
from Factory import Factory

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

factory = Factory("input.txt")

if rank == 0:
    factory.summarize()
    print("\033[4m\033[31mSimulation\033[0m")
    for i in range(factory.production_cycles):
        data = comm.recv(source=1)
        print(f"Master received: {data}")
else:
    # Leaf machines continuously feed products
    if factory.machine_dict[rank].product is not None:
        for i in range(factory.production_cycles):
            factory.machine_dict[rank].send_product(comm)
    # Others wait for the children, perform an operation, and then send the product
    else:
        for i in range(factory.production_cycles):
            factory.machine_dict[rank].receive_products(comm)
            factory.machine_dict[rank].update_state()
            factory.machine_dict[rank].send_product(comm)

MPI.Finalize()