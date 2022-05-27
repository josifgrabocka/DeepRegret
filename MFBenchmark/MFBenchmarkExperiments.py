from MFBenchmark.SMBO import SMBO

# evaluate a list of methods on a benchmark
class MFBenchmarkExperiments:

    def __init__(self):
        pass

    # run the experiments for running a method_class on all the tasks of a metadataset, given a budget
    # returns a list of lists of (config, fidelities, response, elapsed_wallclock_time_in_seconds)
    def run_mf_hpo_benchmark_experiments(metadataset=None, method_class=None, max_trials=None, max_wallclock_time=None):

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

            metadataset_method_hpo_results.append(smbo.run())

        return metadataset_method_hpo_results

    # create the metric time curves given the results
    def metric_time_curves(self, metadataset_method_hpo_results=None, metrics=['regret', 'rank']):
        pass

