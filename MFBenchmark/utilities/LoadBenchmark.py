from MFBenchmark.Benchmark import Benchmark
from MFBenchmark.Benchmark import MetaDataset
from MFBenchmark.Benchmark import Task


# utility script to load a multi-fidelity benchmark
class LoadBenchmark:

    def __init__(self, lc_bench_location=None, taskset_location=None, nb201_location=None):

        metadatasets = []
        if lc_bench_location is not None:
            metadatasets.append(self.load_LCBench(lc_bench_location))
        if taskset_location is not None:
            metadatasets.append(self.load_TaskSet(taskset_location))
        if nb201_location is not None:
            metadatasets.append(self.load_NB201(nb201_location))

        self.benchmark = Benchmark(name='RELEA-MF-Bench', metadatasets=metadatasets)

    # load the LCBench benchmark
    def load_LCBench(self, lc_bench_location):

        tasks = []

        # read the tasks

        evaluations = []
        tasks.append(Task(name="nulltask", evaluations=evaluations))


        return MetaDataset(name='LCBench', tasks=tasks)

    def load_TaskSet(self, taskset_location):
        tasks = []


        # read the tasks

        return MetaDataset(name='TaskSet', tasks=tasks)

    def load_NB201(self, nb201_location):
        md = MetaDataset()

        # read the tasks

        # here load the NB201 metadataset

        return md
