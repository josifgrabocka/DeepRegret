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
        self.name = name
        # the list of evaluations in the form of instances of the Evaluation class
        self.evaluations = evaluations
        # initialize the task_information class that encapsulates the derived information on this task
        self.task_information = TaskInformation(task=self)

    # return the unique configurations of the task
    def fetch_unique_configurations(self):
        # read all the configurations in a list
        configs = []
        for eval in self.evaluations:
            configs.append(eval.configuration)
        # return a list of the unique configurations
        return list(set(configs))

    # return the unique fidelities of a configuraiton, either universally configurations=None,
    # or belonging to one particular configuration
    def fetch_unique_fidelities(self, configuration):
        # read all the configurations in a list
        fidelities = []
        for eval in self.evaluations:
            if eval.configuration == configuration:
                fidelities.append(eval.fidelities)
        # return a list of the unique configurations
        return list(set(fidelities))

    # return the response and runtime of a configuration at the given fidelity, if not found return None
    def evaluate(self, configuration, fidelities):
        for eval in self.evaluations:
            if eval.configuration == configuration and eval.fidelities == fidelities:
                return eval.response, eval.runtime
        return None

# encapsulate the information about a task, that are needed by HPO methods to decide on the initial design,
# what configurations and fidelities to suggest, etc.
class TaskInformation:
    def __init__(self, task=None):
        self.task = task
        # the name of the task
        self.name = None
        # the dimensionality of the design space, a.k.a. number of hyperparameters
        self.design_space_dimensionality=None

        # the list of the unique configurations in the task
        self.feasible_configurations = None
        # the unique fidelities for each configuration
        self.feasible_fidelities = []

        if task is not None:
            self.name = self.task.name
            self.design_space_dimensionality = len(self.task.evaluations[0].configuration)

            # the unique configurations among the ones evaluated in the task, derived from the self.evaluations
            self.feasible_configurations = self.task.fetch_unique_configurations()
            for config in self.feasible_configurations:
                self.feasible_fidelities.append(self.task.fetch_unique_fidelities(config))



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
        return self.configuration, self.fidelities, self.response, self.runtime
