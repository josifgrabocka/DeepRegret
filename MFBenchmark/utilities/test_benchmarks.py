import ConfigSpace

from MFBenchmark.MFBenchmark import Evaluation, Task
from MFBenchmark.utilities.LCBench.api import Benchmark
from pprint import pprint
import ConfigSpace as CSH

lc_bench_dir = "C:/Users/josif/Nextcloud/RELEA/Data/LCBench/six_datasets_lw/six_datasets_lw.json"
bench = Benchmark(lc_bench_dir, cache=False)

lc_tags = bench.get_queriable_tags()

pprint(lc_tags)

dataset_names = bench.get_dataset_names()

pprint(dataset_names)

example_config = bench.query(bench.get_dataset_names()[0], tag='config', config_id=0)

hp_tags = ['batch_size',
                'learning_rate',
                'momentum',
                'weight_decay',
                'num_layers',
                'max_units',
                'max_dropout']

hp_config_space = ConfigSpace.ConfigurationSpace()
hp_config_space.add_hyperparameter(CSH.UniformIntegerHyperparameter('batch_size', lower=16, upper=512, log=True))
hp_config_space.add_hyperparameter(CSH.UniformFloatHyperparameter('learning_rate', lower=0.0001, upper=0.1, log=True))
hp_config_space.add_hyperparameter(CSH.UniformFloatHyperparameter('momentum', lower=0.1, upper=1.0))
hp_config_space.add_hyperparameter(CSH.UniformFloatHyperparameter('weight_decay', lower=0.00001, upper=0.1, log=True))
hp_config_space.add_hyperparameter(CSH.UniformIntegerHyperparameter('num_layers', lower=1, upper=5))
hp_config_space.add_hyperparameter(CSH.UniformFloatHyperparameter('max_units', lower=64, upper=1024, log=True))
hp_config_space.add_hyperparameter(CSH.UniformFloatHyperparameter('max_dropout', lower=0.0, upper=1.0))

fidelity_tags = ['epoch']

fidelity_config_space = ConfigSpace.ConfigurationSpace()
fidelity_config_space.add_hyperparameter(CSH.UniformIntegerHyperparameter('epoch', lower=1, upper=50))

print(hp_config_space)

# create empty dictionary for the sets of the unique values for each hyperparameters
unique_hp_values = {}
for hp_name in example_config:
    unique_hp_values[hp_name] = set()

print(unique_hp_values)

# iterate through all the tasks and add the values to the sets
for dataset_name in dataset_names:

    # the number of evaluated configurations for that dataset
    n_configs = bench.get_number_of_configs(dataset_name=dataset_name)

    # the list of evaluations
    evals = []

    for config_idx in range(n_configs):
        config = bench.query(dataset_name=dataset_name, tag='config', config_id=config_idx)

        epoch_series = bench.query(dataset_name=dataset_name, tag='epoch', config_id=config_idx)
        runtime = bench.query(dataset_name=dataset_name, tag='time', config_id=config_idx)
        response = bench.query(dataset_name=dataset_name, tag='Train/test_balanced_accuracy', config_id=config_idx)
        aux_response1 = bench.query(dataset_name=dataset_name, tag='Train/train_accuracy', config_id=config_idx)
        aux_response2 = bench.query(dataset_name=dataset_name, tag='Train/train_cross_entropy', config_id=config_idx)
        aux_response3 = bench.query(dataset_name=dataset_name, tag='Train/train_balanced_accuracy', config_id=config_idx)

        filtered_configs = {hp_name: config[hp_name] for hp_name in hp_tags}
        config = CSH.Configuration(configuration_space=hp_config_space, values=filtered_configs)

        for i in range(len(epoch_series)):

            fidelities = {'epoch': epoch_series[i]}

            fid = CSH.Configuration(configuration_space=fidelity_config_space, values=fidelities)



        print(config)
