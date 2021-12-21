from MFBenchmark.SMBO import SMBO

# evaluate a list of methods on a benchmark
class Experiments:

    def __init__(self):
        pass

    # run all the experiments for the
    def run_hpo_experiments(metadataset=None, method_class=None, max_trials=None, max_wallclock_time=None):

        metadataset_method_hpo_results = []

        for task in metadataset.tasks:

            # create an instance of the method class with the task information, config and fidelities spaces,
            # as well as the budget information
            method = method_class(taskinformation=task.task_information,
                                  config_space=metadataset.config_space,
                                  fidel_space=metadataset.fidel_space,
                                  max_trials=max_trials,
                                  max_wallclock_time=max_wallclock_time)

            # create an instance of the SMBO class with the task, the method as well as the budget information
            smbo = SMBO(task=task, method=method, max_trials=max_trials, max_wallclock_time=max_wallclock_time)

            metadataset_method_hpo_results.append(smbo.run_hpo())

        return metadataset_method_hpo_results