import string_util

# This class represents a single machine in the factory.
# Important data fields are as follow:
# id: the id of the machine (need to map to process ranks)
# pid: machine id of the parent
# children: list of machine ids of the children to this machine
# next_op: the next_operation to be performed with this machine
# product: the current product that machine has inside it

class Machine():
    # Straightforward constructor
    def __init__(self, id, pid, next_op):
        self.id = id
        self.pid = pid
        self.children = []
        self.next_op = next_op
        self.product = None

    # Wait for all the children to send their product
    # And then perform the next_op
    def receive_products(self, comm):
        data_list = []
        for child in self.children:
            data = comm.recv(source=child)
            data_list.append(data)
        self.product = "".join(data_list)
        # Perform the necessary operation.
        if self.next_op == "split":
            self.product = string_util.split(self.product)
        elif self.next_op == "chop":
            self.product = string_util.chop(self.product)
        elif self.next_op == "enhance":
            self.product = string_util.enhance(self.product)
        elif self.next_op == "trim":
            self.product = string_util.trim(self.product)
        elif self.next_op == "reverse":
            self.product = string_util.reverse(self.product) 
        else: 
            pass       

    # For updating next operation and maintenance checks
    def update_state(self):
        if self.id % 2 == 0:
            if self.next_op == "split":
                self.next_op = "chop"
            elif self.next_op == "chop":
                self.next_op = "enhance"
            else:
                self.next_op = "split" 
        else:
            if self.next_op == "trim":
                self.next_op = "reverse"
            else:
                self.next_op = "trim"

    # Send the prodcut to parent
    def send_product(self, comm):
        if self.pid is not None:
            # print(f"{self.id} is sending {self.product} to {self.pid}")
            comm.send(self.product, dest=self.pid)