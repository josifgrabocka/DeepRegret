import datetime

class SMBO:

    def __init__(self, task=None, method=None, max_trials=None, max_wallclock_time=None):
        self.task = task
        self.method = method
        self.max_num_trials = max_trials
        self.max_wallclock_time = max_wallclock_time
        self.history_configurations = []
        self.history_fidelities = []
        self.history_reponses = []
        self.history_elapsed_runtimes = []
        self.num_parallel_configurations = 1

    # run the HPO
    def run_hpo(self):

        # initialize the number of trials and the elapsed wallclock time
        trial=0
        elapsed_wallclock_time = 0

        # INITIALIZATION
        # get the suggested initial design (configurations,fidelities) from the method
        start_time = datetime.datetime.now()
        initial_configurations, initial_fidelities = self.method.suggest_initial()
        end_time = datetime.datetime.now()
        elapsed_wallclock_time += (end_time - start_time).total_seconds()

        initial_responses = []
        initial_runtimes = []
        # query the task to retrieve the reponse and runtime of the initial configs and fidelities
        for conf, fid in zip(initial_configurations, initial_fidelities):
            response, runtime = self.task.evaluate(configuration=conf, fidelities=fid)
            initial_responses.append(response)
            initial_runtimes.append(runtime)
            # update the elapsed wallclock time
            elapsed_wallclock_time += runtime
            # update the history
            self.history_configurations.append(conf)
            self.history_fidelities.append(fid)
            self.history_reponses.append(response)
            self.history_elapsed_runtimes.append(elapsed_wallclock_time)

        # return the observation of the initial design to the method, measure the elapsed time
        start_time = datetime.datetime.now()
        self.method.observe_initial(configurations=initial_configurations, fidelities=initial_fidelities,
                                    responses=initial_responses, runtimes=initial_runtimes)
        end_time = datetime.datetime.now()
        elapsed_wallclock_time += (end_time - start_time).total_seconds()

        # HPO trial steps
        while True:
            # check termination conditions
            # check if the maximum number of trials is exceeded
            if self.max_num_trials is not None:
                if trial > self.max_num_trials:
                    break
            # check if the total wall clock time is exceeded
            if self.max_wallclock_time is not None:
                if elapsed_wallclock_time > self.max_wallclock_time:
                    break

            # get the suggested configurations and fidelities from the method
            start_time = datetime.datetime.now()
            configurations, fidelities = self.method.suggest(self.num_parallel_configurations)
            end_time = datetime.datetime.now()
            elapsed_wallclock_time += (end_time - start_time).total_seconds()

            responses = []
            runtimes = []
            # query the task to retrieve the reponse and runtime of the suggested configurations
            for conf, fid in zip(configurations, fidelities):
                response, runtime = self.task.evaluate(configuration=conf, fidelities=fid)
                responses.append(response)
                runtimes.append(runtime)
                # update the elapsed wallclock time
                elapsed_wallclock_time += runtime
                # update the history
                self.history_configurations.append(conf)
                self.history_fidelities.append(fid)
                self.history_reponses.append(response)
                self.history_elapsed_runtimes.append(elapsed_wallclock_time)

            # return the observation of the initial design to the method, measure the elapsed time
            start_time = datetime.datetime.now()
            self.method.observe(configurations=configurations, fidelities=fidelities,
                                responses=initial_responses, runtimes=initial_runtimes)
            end_time = datetime.datetime.now()
            elapsed_wallclock_time += (end_time - start_time).total_seconds()

