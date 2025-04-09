from canproc.runners import DaskRunner
from canproc import DAG
from dask.distributed import LocalCluster


class DaskDistributedRunner(DaskRunner):

    def __init__(
        self,
        processes=True,
        workers=1,
        threads_per_worker=1,
        **kwargs,
    ):

        workers = kwargs.pop("workers", workers)
        threads_per_worker = kwargs.pop("threads_per_worker", threads_per_worker)
        processes = kwargs.pop("processes", processes)

        self.cluster = LocalCluster(
            processes=processes, n_workers=workers, threads_per_worker=threads_per_worker, **kwargs
        )

        self.client = self.cluster.get_client()
        self.scheduler = self.client.get
