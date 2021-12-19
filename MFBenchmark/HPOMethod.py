
# an abstract HPO method
class HPOMethod:

    # initialize a HPO method providing the initial setup as:
    # init_configurations: a list of configuration vectors
    def __init__(self, task_information):
        self.task_information = task_information

    # suggest the initial configuration to try
    # returns a list of tuples (configurations, fidelities)
    # this step is commonly referred to as the acquisition function
    def suggest_initial(self):
        pass
    # observe the response of the initial configurations from self.suggest_initial
    # returns a list of tuples (configurations, fidelities), where the length of the list is num_configurations
    def observe_initial(self, configurations, fidelities, responses, runtimes):
        pass

    # suggest a number of next configurations to try
    # returns a list of tuples (configurations, fidelities), where the length of the list is num_configurations
    # this step is commonly referred to as the acquisition function
    # this method should be run after suggest_initial
    def suggest(self, num_configurations=1):
        return None

    # provide the evaluated configurations to the method as observations
    # this step is commonly referred as surrogate fitting and updating the history
    def observe(self, configurations, fidelities, responses, runtimes):
        pass
