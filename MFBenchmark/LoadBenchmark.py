from MFBenchmark.Benchmark import Benchmark
from MFBenchmark.Benchmark import MetaDataset


# utility script to load a multi-fidelity benchmark

class LoadBenchmark:

    def __init__(self, lc_bench_location=None, taskset_location=None, nb201_location=None):
        self.benchmark = Benchmark()

        if lc_bench_location is not None:
            self.benchmark.metadatasets.append(self.load_LCBench(lc_bench_location))
        if lc_bench_location is not None:
            self.benchmark.metadatasets.append(self.load_TaskSet(lc_bench_location))
        if lc_bench_location is not None:
            self.benchmark.metadatasets.append(self.load_NB201(lc_bench_location))

    # load the LCBench benchmark
    def load_LCBench(self, lc_bench_location):
        md = MetaDataset()

        # here load the lcbench metadataset

        return md

    def load_TaskSet(self, taskset_location):
        md = MetaDataset()

        # here load the taskset metadataset

        return md

    def load_NB201(self, nb201_location):
        md = MetaDataset()

        # here load the NB201 metadataset

        return md

# load the Taskset benchmark
