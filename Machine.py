import string_util

# This class represents a single machine in the factory.

# Important data fields are as follow:
# id: the id of the machine (need to map to process ranks)
# pid: machine id of the parent
# children: list of machine ids of the children to this machine
# next_op: the next_operation to be performed with this machine
# product: the current product that machine has inside it

# Important data fields are as follows:
# receive_products(self, comm): wait for all for all of a machines
# children to send their products.
# update_state(self): update state and keep account of maintenance costs
# Send a maintenance signal when necessary.
# send_product(self, comm): send the current product to your parent.

class Machine():
    # Straightforward constructor
    def __init__(self, id, pid, next_op, threshold, wear_dict):
        self.id = id
        self.pid = pid
        self.children = []
        self.next_op = next_op
        self.product = None
        self.message = None
        self.wear = 0
        self.threshold = threshold
        self.wear_dict = wear_dict
        self.cycle = 1

    # Wait for all the children to send their product
    # And then perform the next_op
    def receive_products(self, comm):
        data_list = []
        for child in self.children:
            data = comm.recv(source=child)
            data_list.append([child, data])
        sorted_data = sorted(data_list, key=lambda x:x[0])
        data_list = [pair[1] for pair in sorted_data]
        self.product = "".join(data_list)      

    # For updating next operation and maintenance checks
    def update_state(self, comm):
        # Accumulate wear
        if self.next_op is not None:
            self.wear += self.wear_dict[self.next_op]
            if self.wear >= self.threshold:
                cost = (self.wear - self.threshold + 1) * self.wear_dict[self.next_op]
                comm.isend(f"{self.id}-{cost}-{self.cycle}", dest=0, tag=13)
                self.wear = 0
        self.cycle += 1

        # Perform the necessary operation.
        if self.next_op == "split":
            self.message = string_util.split(self.product)
        elif self.next_op == "chop":
            self.message = string_util.chop(self.product)
        elif self.next_op == "enhance":
            self.message = string_util.enhance(self.product)
        elif self.next_op == "trim":
            self.message = string_util.trim(self.product)
        elif self.next_op == "reverse":
            self.message = string_util.reverse(self.product) 
        else: 
            self.message = self.product 

        if self.id % 2 == 0:
            if self.next_op == "split":
                self.next_op = "chop"
            elif self.next_op == "chop":
                self.next_op = "enhance"
            elif self.next_op == "enhance":
                self.next_op = "split" 
            else:
                pass
        else:
            if self.next_op == "trim":
                self.next_op = "reverse"
            elif self.next_op == "reverse":
                self.next_op = "trim"
            else:
                pass

    # Send the prodcut to parent
    def send_product(self, comm):
        if self.pid is not None:
            # print(f"{self.id} is sending {self.message} to {self.pid}")
            comm.send(self.message, dest=self.pid, tag=0)