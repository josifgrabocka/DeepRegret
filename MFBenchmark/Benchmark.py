
# a benchmark is a collection of meta-datasets
class Benchmark:
    def __init__(self):
        self.name = ''
        # the collection of meta-datasets
        self.metadatasets = []


# a meta-dataset is a collection of evaluations in different tasks, i.e. datasets
class MetaDataset:
    def __init__(self):
        self.name = ''
        # the list of evaluations in the form of instances of the Evaluation class
        self.tasks = []


# a task represents the evaluations of configurations from a search space on a dataset
# it is a collection of evaluations of the form (configurations, responses)
class Task:
    def __init__(self):
        self.name = ''
        # the list of evaluations in the form of instances of the Evaluation class
        self.evaluations = []
        # the unique configurations among the ones evaluated in the meta-dataset, derived from the self.evaluations
        self.unique_configurations = []

    # return the response of a configuration at the given fidelity
    def evaluate(self, configuration, fidelity):
        pass

    # returns the lowest response at the given fidelity among all the configurations from the evaluations
    def best_response(self, fidelity):
        pass

    # returns a random sample of evaluations specified with num_evaluations
    # if sample_fidelities=True, the method cuts the learning curves randomly and returns the evaluations
    # of the first M fidelities, where M is a random number between 1 and the max. evaluated fidelity
    def sample(self, num_evaluations, sample_fidelities=False):
        pass

# an evaluation is a tuple of (configuration, fidelities, responses), where
# fidelities indicate the budget for which the configuration was evaluated
# responses indicate the response of evaluating a configuration at the respective fidelity
class Evaluation:
    def __init__(self):
        self.configuration = None
        self.fidelities = None
        self.responses = None

    def __call__(self):
        return self.configuration, self.fidelities, self.responses
