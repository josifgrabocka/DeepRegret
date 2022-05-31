from MFBenchmark.methods.AbstractHPOMethod import AbstractHPOMethod
import random

class RandomDiscreteSearchMF(AbstractHPOMethod):

    # initialize a HPO method providing task information and the budget as contructor informaiton
    def __init__(self, task_information, config_space=None, fidel_space=None, max_trials=None, max_wallclock_time=None):

        AbstractHPOMethod.__init__(self, task_information=task_information,
                                   config_space=config_space,
                                   fidel_space=fidel_space,
                                   max_trials=max_trials,
                                   max_wallclock_time=max_wallclock_time)

    # suggests a list of next configurations, and for what fidelity to try those configurations
    # returns a list of tuples (configurations, fidelities), where the length of the list is num_configurations
    # this step is commonly referred to as the acquisition function
    # this method should be run after suggest_initial
    def suggest(self):

        random_config = random.choice(self.task_information.feasible_configurations)
        fids = self.task_information.feasible_fidelities_per_config[random_config]
        random_fid = random.choice(tuple(fids))

        return [(random_config, random_fid)]

    # provide the evaluated configurations to the method as observations
    # this step is commonly referred as surrogate fitting and updating the history
    def observe(self, configurations, fidelities, responses, runtimes):
        pass
