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
# config_space: is an instance from the https://automl.github.io/ConfigSpace/master/ class
# evaluations: is a list of Evaluation class instances
class Task:
    def __init__(self, name=None, config_space=None, evaluations=None, continuous_surrogate=None):
        self.name = name
        # the design space: descriptions of each hyperparameter
        self.config_space = config_space
        # the list of evaluations in the form of instances of the Evaluation class
        self.evaluations = evaluations

        # is the task a continuous or discrete one, if continuous
        self.is_continuous = False
        if evaluations is None and continuous_surrogate is not None:
            self.is_continuous = True
            self.continuous_surrogate = continuous_surrogate

        # initialize the task_information class that encapsulates the derived information on this task
        self.task_information = TaskInformation(task=self, is_continuous=self.is_continuous)

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
        # querying the continuous surrogate
        if self.is_continuous:
            return None
        else:
            for eval in self.evaluations:
                if eval.configuration == configuration and eval.fidelities == fidelities:
                    return eval.response, eval.runtime
            # evaluation not found
            return None


# encapsulate the information about a task, that are needed by HPO methods to decide on the initial design,
# what configurations and fidelities to suggest, etc.
class TaskInformation:
    def __init__(self, task=None, is_continuous=False):
        self.task = task
        self.is_continuous = is_continuous
        # the configuration space
        self.config_space = self.task.config_space

        if task is not None:

            # the feasible configurations for non-continuous spaces
            if not self.is_continuous:

                # the list of the unique configurations in the task
                self.feasible_configurations = None
                # the unique fidelities for each configuration
                self.feasible_fidelities = []

                # the unique configurations among the ones evaluated in the task, derived from the self.evaluations
                self.feasible_configurations = self.task.fetch_unique_configurations()
                for config in self.feasible_configurations:
                    self.feasible_fidelities.append(self.task.fetch_unique_fidelities(config))


# an evaluation is a tuple of (configuration, fidelities, response, runtime), where
# configuration is a Configuration from the ConfigSpace library
# fidelities is a [list of floats] when many-fidelities are used, OR a single [float] if just one fidelity is used
# response [float] indicate the response of evaluating a configuration at the respective fidelity
# runtime [float] indicate the wallclock runtime in seconds of evaluating a configuration at the respective fidelity
class Evaluation:
    def __init__(self, configuration=None, fidelities=None, response=None, runtime=None):
        self.configuration = configuration
        self.fidelities = fidelities
        self.response = response
        self.runtime = runtime

    def __call__(self):
        return self.configuration, self.fidelities, self.response, self.runtime
