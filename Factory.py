from Machine import Machine

class Factory:
    # Create a factory using the information in the input file
    def __init__(self, input_file_path):
        self.wear_factor_dict = {
            "enhance": None,
            "reverse": None,
            "chop": None,
            "trim": None,
            "split": None
        }
        self.machine_list = []
        with open(input_file_path, "r") as input_file:
            self.machine_count = int(input_file.readline().strip())
            self.production_cycles = int(input_file.readline().strip())
            wear_factor_list = [int(i) for i in input_file.readline().strip().split()]
            for key, value in zip(self.wear_factor_dict.keys(), wear_factor_list):
                self.wear_factor_dict[key] = value
            self.maintenance_threshold = int(input_file.readline().strip())
            for i in range(self.machine_count-1):
                machine_init_info = input_file.readline().strip().split()
                self.machine_list.append(Machine(int(machine_init_info[0]), int(machine_init_info[1]), machine_init_info[2]))
            parent_machines = set([machine.pid for machine in self.machine_list])
            leaf_machines = set([machine.id for machine in self.machine_list]).difference(parent_machines)
            for id in leaf_machines:
                for machine in self.machine_list:
                    if machine.id == id:
                        machine.product = input_file.readline().strip()

        # Creating the dictionary that maps the ids to actual objects
        self.machine_dict = {}
        for machine in self.machine_list:
            self.machine_dict[machine.id] = machine
        for machine in self.machine_list:
            if machine.pid not in self.machine_dict:
                self.machine_dict[machine.pid] = Machine(machine.pid, 0, None)
        for machine in self.machine_list:
            self.machine_dict[machine.pid].children.append(machine.id)
    
    # Neat print-out of the details of the factory object.
    def summarize(self):
        print("\033[4m\033[32mFactory Summary\033[0m")
        print(f"Machine Count: {self.machine_count}")
        print(f"Profduction Cycles: {self.production_cycles}")
        print(f"Wear Factors:")
        for key in self.wear_factor_dict:
            print(f"\t{key}:".ljust(10) + f"{self.wear_factor_dict[key]}")
        print(f"Maintenance Threshold: {self.maintenance_threshold}")
        print("\033[4m\033[32mMachines\033[0m")
        print(f"\033[4m{'ID'.center(10)}{'Parent'.center(10)}{'Children'.center(16)}\033[0m")
        for id in self.machine_dict:
            print(f"{str(id).center(10)}{str(self.machine_dict[id].pid).center(10)}\t{str(self.machine_dict[id].children).ljust(10)}")
