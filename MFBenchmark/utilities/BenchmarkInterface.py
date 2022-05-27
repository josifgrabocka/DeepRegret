from MFBenchmark.MFBenchmark import Evaluation, Task, MetaDataset, MFBenchmark
import ConfigSpace as CSH
from MFBenchmark.utilities.LCBench.api import Benchmark

# utility script to load a multi-fidelity benchmark
class BenchmarkInterface:

    def __init__(self, lc_bench_location=None, taskset_location=None, nb201_location=None):

        metadatasets = []
        if lc_bench_location is not None:
            metadatasets.append(self.load_LCBench(lc_bench_location))
        if taskset_location is not None:
            metadatasets.append(self.load_TaskSet(taskset_location))
        if nb201_location is not None:
            metadatasets.append(self.load_NB201(nb201_location))

        self.benchmark = MFBenchmark(name='RELEA-MF-Bench', metadatasets=metadatasets)

    # load the LCBench benchmark
    def load_LCBench(self, lc_bench_location):

        # read the lc bench
        bench = Benchmark(lc_bench_location, cache=False)
        # fetch the list of datasets
        dataset_names = bench.get_dataset_names()

        # the hyperparameter tags for the non-constant hyperparameters
        hp_tags = ['batch_size',
                   'learning_rate',
                   'momentum',
                   'weight_decay',
                   'num_layers',
                   'max_units',
                   'max_dropout']

        # define the hyperparameter configuration space
        hp_config_space = CSH.ConfigurationSpace()
        hp_config_space.add_hyperparameter(CSH.UniformIntegerHyperparameter('batch_size', lower=16, upper=512, log=True))
        hp_config_space.add_hyperparameter(CSH.UniformFloatHyperparameter('learning_rate', lower=0.0001, upper=0.1, log=True))
        hp_config_space.add_hyperparameter(CSH.UniformFloatHyperparameter('momentum', lower=0.1, upper=1.0))
        hp_config_space.add_hyperparameter(CSH.UniformFloatHyperparameter('weight_decay', lower=0.00001, upper=0.1, log=True))
        hp_config_space.add_hyperparameter(CSH.UniformIntegerHyperparameter('num_layers', lower=1, upper=5))
        hp_config_space.add_hyperparameter(CSH.UniformFloatHyperparameter('max_units', lower=64, upper=1024, log=True))
        hp_config_space.add_hyperparameter(CSH.UniformFloatHyperparameter('max_dropout', lower=0.0, upper=1.0))
        print(hp_config_space)

        # define the fidelity space
        fidelity_config_space = CSH.ConfigurationSpace()
        fidelity_config_space.add_hyperparameter(CSH.UniformIntegerHyperparameter('epoch', lower=0, upper=51))

        # iterate through all the tasks and add the values to the sets
        tasks = []
        for dataset_name in dataset_names:

            # the number of evaluated configurations for that dataset
            n_configs = bench.get_number_of_configs(dataset_name=dataset_name)

            print(f'Loading dataset {dataset_name} with {n_configs} configurations')
            # the list of evaluations
            evals = []

            for config_idx in range(n_configs):
                config = bench.query(dataset_name=dataset_name, tag='config', config_id=config_idx)
                epoch_series = bench.query(dataset_name=dataset_name, tag='epoch', config_id=config_idx)
                runtime_series = bench.query(dataset_name=dataset_name, tag='time', config_id=config_idx)

                val_response_series = bench.query(dataset_name=dataset_name, tag='Train/val_balanced_accuracy', config_id=config_idx)
                test_response_series = bench.query(dataset_name=dataset_name, tag='Train/test_balanced_accuracy', config_id=config_idx)
                # fetch three additional
                aux_responses_series = [
                    bench.query(dataset_name=dataset_name, tag='Train/train_accuracy', config_id=config_idx),
                    bench.query(dataset_name=dataset_name, tag='Train/train_balanced_accuracy', config_id=config_idx),
                    bench.query(dataset_name=dataset_name, tag='Train/train_cross_entropy', config_id=config_idx),
                    bench.query(dataset_name=dataset_name, tag='Train/val_cross_entropy', config_id=config_idx)]

                filtered_configs = {hp_name: config[hp_name] for hp_name in hp_tags}
                config = CSH.Configuration(configuration_space=hp_config_space, values=filtered_configs)

                for i in range(len(epoch_series)):

                    try:
                        fid = CSH.Configuration(configuration_space=fidelity_config_space, values={'epoch': epoch_series[i]})
                        val_response = val_response_series[i]
                        test_response = test_response_series[i]
                        runtime = runtime_series[i]
                        # store the auxiliary response
                        auxiliary_responses = []
                        for aux_response_series in aux_responses_series:
                            auxiliary_responses.append(aux_response_series[i])

                        evals.append(Evaluation(configuration=config,
                                                fidelities=fid,
                                                val_response=val_response,
                                                test_response=test_response,
                                                runtime=runtime,
                                                auxiliary_responses=auxiliary_responses))

                    except ValueError as ve:
                        print(ve)

            tasks.append(Task(name=dataset_name, evaluations=evals))

        return MetaDataset(name='lcbench', config_space=hp_config_space, fidel_space=fidelity_config_space, tasks=tasks)

    def load_TaskSet(self, taskset_location):
        tasks = []


        # read the tasks

        return MetaDataset(name='TaskSet', tasks=tasks)

    def load_NB201(self, nb201_location):
        md = MetaDataset()

        # read the tasks

        # here load the NB201 metadataset

        return md

