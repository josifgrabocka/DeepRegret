import logging

# a benchmark is a collection of meta-datasets
class Benchmark:
    def __init__(self, name=None, metadatasets=None):
        self.name = name
        # the collection of meta-datasets
        self.metadatasets = metadatasets

# a meta-dataset is a collection of evaluations in different tasks, i.e. datasets
class MetaDataset:
    def __init__(self, name=None, tasks=None):
        self.name = name
        # the list of evaluations in the form of instances of the Evaluation class
        self.tasks = tasks

# a task represents the evaluations of configurations from a search space on a dataset
# it is a collection of evaluations of the form (configurations, responses)
class Task:
    def __init__(self, name=None, evaluations=None):
        self.name = name
        # the list of evaluations in the form of instances of the Evaluation class
        self.evaluations = evaluations
        # the unique configurations among the ones evaluated in the meta-dataset, derived from the self.evaluations
        self.unique_configurations = self.compute_unique_configurations()

        self.num_total_evaluations = len(self.evaluations)
        self.num_unique_configurations = len(self.unique_configurations)

        # information line on the task initialization
        logging.info('Initialized Task', self.name, 'with', self.num_total_evaluations, 'total evaluations, ',
              self.num_unique_configurations, 'unique configurations')


        # count the unique configurations of the task
    def compute_unique_configurations(self):
        # read all the configurations in a list
        self.configs = []
        for eval in self.evaluations:
            self.configs.append(eval.configuration)
        # return a list of the unique configurations
        return list(set(self.configs))

    # return the response of a configuration at the given fidelity, if not found return None
    def evaluate(self, configuration, fidelities):
        for eval in self.evaluations:
            if eval.configuration == configuration and eval.fidelities == fidelities:
                return eval.response
        return None

    # returns the lowest response at the given fidelities among all the configurations from the evaluations
    def best_response(self, fidelities):
        pass

    # returns a random sample of evaluations specified with num_evaluations
    # if sample_fidelities=True, the method cuts the learning curves randomly and returns the evaluations
    # of the first M fidelities, where M is a random number between 1 and the max. evaluated fidelity
    def sample(self, num_evaluations):

        pass

# an evaluation is a tuple of (configuration, fidelities, responses), where
# configuration is a vector of the hyperparameter values
# fidelities is a vector of the used fidenities
# responses indicate the response of evaluating a configuration at the respective fidelity
class Evaluation:
    def __init__(self, configuration=None, fidelities=None, response=None):
        self.configuration = configuration
        self.fidelities = fidelities
        self.response = response

    def __call__(self):
        return self.configuration, self.fidelities, self.response
