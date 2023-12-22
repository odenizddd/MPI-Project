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
        data = comm.recv(source=1, tag=0)
        print(f"Master received: {data}")
    while True:
        # Check if there is a message to receive
        status = MPI.Status()
        message_available = comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)

        if message_available:
            source = status.Get_source()
            tag = status.Get_tag()

            # Non-blocking receive
            request = comm.irecv(source=source, tag=tag)
            
            # Wait for the communication to complete
            received_data = request.wait()

            # Print the received message
            print(f"{received_data}")
        else:
            # No more messages, break out of the loop
            break
else:
    # Leaf machines continuously feed products
    if factory.machine_dict[rank].product is not None:
        for i in range(factory.production_cycles):
            factory.machine_dict[rank].update_state(comm)
            factory.machine_dict[rank].send_product(comm)
    # Others wait for the children, perform an operation, and then send the product
    else:
        for i in range(factory.production_cycles):
            factory.machine_dict[rank].receive_products(comm)
            factory.machine_dict[rank].update_state(comm)
            factory.machine_dict[rank].send_product(comm)

MPI.Finalize()