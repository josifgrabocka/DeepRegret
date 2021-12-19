import logging
import sys

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

        # the list of evaluations in the form of instances of the Evaluation class
        self.evaluations = evaluations

        # initialize the task_information class that encapsulates the derived information on this task
        self.task_information = TaskInformation()
        self.task_information.name = name
        self.task_information.num_total_evaluations = len(self.evaluations)
        self.task_information.design_space_dimensionality = len(self.evaluations[0].configuration)

        # the unique configurations among the ones evaluated in the meta-dataset, derived from the self.evaluations
        self.task_information.unique_configurations = self.fetch_unique_configurations()
        self.task_information.num_unique_configurations = len(self.task_information.unique_configurations)

        # the unique fidelities among the ones evaluated in the meta-dataset, derived from the self.evaluations
        self.task_information.unique_fidelities = self.fetch_unique_fidelities()
        self.task_information.num_unique_fidelities = len(self.task_information.unique_fidelities)
        # for each unique fidelity fetch the min and max response across all the evaluations
        for fidelities in self.task_information.unique_fidelities:
            self.task_information.min_response_per_unique_fidelities.append(self.min_response(fidelities))
            self.task_information.max_response_per_unique_fidelities.append(self.max_response(fidelities))

        # information line on the task initialization
        logging.info('Initialized Task', self.task_information.name, 'with',
                     self.task_information.num_total_evaluations, 'total evaluations, ',
                     self.task_information.num_unique_configurations, 'unique configurations')

    # return the unique configurations of the task
    def fetch_unique_configurations(self):
        # read all the configurations in a list
        configs = []
        for eval in self.evaluations:
            configs.append(eval.configuration)
        # return a list of the unique configurations
        return list(set(configs))

    # return the unique configurations of the task
    def fetch_unique_fidelities(self):
        # read all the configurations in a list
        fidelities = []
        for eval in self.evaluations:
            fidelities.append(eval.configuration)
        # return a list of the unique configurations
        return list(set(fidelities))

    # return the response and runtime of a configuration at the given fidelity, if not found return None
    def evaluate(self, configuration, fidelities):
        for eval in self.evaluations:
            if eval.configuration == configuration and eval.fidelities == fidelities:
                return eval.response, eval.runtime
        return None

    # returns the highest response at the given fidelities among all the configurations from the evaluations
    def max_response(self, fidelities):
        max_response = -sys.float_info.max
        for eval in self.evaluations:
            if eval.fidelities == fidelities and eval.response > max_response:
                max_response = eval.response
        return max_response

    # returns the highest response at the given fidelities among all the configurations from the evaluations
    def min_response(self, fidelities):
        min_response = sys.float_info.max
        for eval in self.evaluations:
            if eval.fidelities == fidelities and eval.response < min_response:
                min_response = eval.response
        return min_response

    # returns a random sample of evaluations specified with num_evaluations
    # if sample_fidelities=True, the method cuts the learning curves randomly and returns the evaluations
    # of the first M fidelities, where M is a random number between 1 and the max. evaluated fidelity
    def sample(self, num_evaluations):

        pass

# encapsulate the information about a task
class TaskInformation:
    def __init__(self):
        # the name of the task
        self.name = None
        # the dimensionality of the design space, a.k.a. number of hyperparameters
        self.design_space_dimensionality=None
        # the total number of evaluations in the task
        self.num_total_evaluations = None

        # the list of the unique configuraitons in the task
        self.unique_configurations = None
        # the number of unique configurations
        self.num_unique_configurations = None

        # a list of the unique fidelities in the task
        self.unique_fidelities = None
        # the number of unique fidelities
        self.num_unique_fidelities = None
        # the min and max reponse observed for each unique fidelities
        # the indices of self.unique_fidelities semantically match the indices of
        # self.min_response_per_unique_fidelities and self.max_response_per_unique_fidelities
        self.min_response_per_unique_fidelities = None
        self.max_response_per_unique_fidelities = None


# an evaluation is a tuple of (configuration, fidelities, responses), where
# configuration is a [list of floats] representing the hyperparameter values
# fidelities is a [list of floats] when many-fidelities are used, OR a single [float] if just one fidelity is used
# response [float] indicate the response of evaluating a configuration at the respective fidelity
# runtime [float] indicate the wallclock runtime of evaluating a configuration at the respective fidelity
# Note: runtimes are in SECONDS
class Evaluation:
    def __init__(self, configuration=None, fidelities=None, response=None, runtime=None):
        self.configuration = configuration
        self.fidelities = fidelities
        self.response = response
        self.runtime = runtime

    def __call__(self):
        return self.configuration, self.fidelities, self.response
