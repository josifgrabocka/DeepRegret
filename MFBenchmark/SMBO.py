import datetime

# a sequential model based optimization algorithm that needs as an input
# a task, a method and the budget information, as the max_trial, or max_wallclock_time, or both whichever is reached first
class SMBO:

    def __init__(self, task=None, method=None, max_trials=None, max_wallclock_time=None):
        # store the task and the method
        self.task = task
        self.method = method
        # store the budget
        self.max_num_trials = max_trials
        self.max_wallclock_time = max_wallclock_time

    # run the HPO
    # returns a list of (configuration, fidelities, response, elapsed_time)
    def run_hpo(self):

        # the HPO history of every step, the list of configurations, the associated fidelities,
        # and the corresponding reponses and wallclock times
        hpo_history = []

        # initialize the number of trials and the elapsed wallclock time
        elapsed_num_trials = 0
        elapsed_wallclock_time = 0

        # HPO elapsed_num_trials steps
        while True:
            # check termination conditions
            # check if the maximum number of trials is exceeded
            if self.max_num_trials is not None:
                if elapsed_num_trials > self.max_num_trials:
                    break
            # check if the total wall clock time is exceeded
            if self.max_wallclock_time is not None:
                if elapsed_wallclock_time > self.max_wallclock_time:
                    break

            # get the suggested configurations and fidelities from the method
            start_time = datetime.datetime.now()
            configurations, fidelities = self.method.suggest()
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
                # update the number of trials
                elapsed_num_trials += 1
                # update the history
                hpo_history.append((conf, fid, response, elapsed_wallclock_time))

            # return the observation of the initial design to the method, measure the elapsed time
            start_time = datetime.datetime.now()
            self.method.observe(configurations=configurations, fidelities=fidelities,
                                responses=responses, runtimes=runtimes)
            end_time = datetime.datetime.now()
            elapsed_wallclock_time += (end_time - start_time).total_seconds()

        # return the hpo history
        return hpo_history