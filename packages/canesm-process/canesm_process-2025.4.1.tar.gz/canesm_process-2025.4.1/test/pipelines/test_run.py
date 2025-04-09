from canproc.pipelines import Pipeline

# from dask.dot import dot_graph
from canproc.runners import DaskRunner
import pytest
import os


@pytest.mark.skip(reason="requires access to science")
def test_run_pipeline(
    client=None, report=True, filename: str | None = None, scheduler: str = "threads"
):

    import time
    from dask.diagnostics import Profiler, ResourceProfiler, CacheProfiler, visualize
    from dask.distributed import performance_report

    # qsub -I -lselect=1:ncpus=80:mem=175gb -lplace=scatter -Wumask=022 -S/bin/bash -qdevelopment -lwalltime=02:00:00
    # config = r"/space/hall5/sitestore/eccc/crd/ccrn/users/rvs001/templates/canproc_tests/metadata/tables/core_cmip6.yaml"
    # config = r"/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/software/pipelines/canesm-processor/test/tables/core_cmip6.yaml"
    config = r"/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/software/canesm-processor/config/cmip/dev_cmip6.yaml"
    # config = r"/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/software/pipelines/canesm-processor/test/tables/"
    input_dir = r"/space/hall5/sitestore/eccc/crd/ccrn/users/rvs001/data/jcl-diag-test-a-009/1.0x1.0_monthly/ncdir"
    input_dir = "/fs/site6/eccc/crd/ccrn/users/aya001/canesm_runs/v6b1-lakendg-aya/data"
    # output_dir = r"/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/canproc/jcl-diag-test-a-009-cmip"
    output_dir = "/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/canproc/v6b1-lakendg-aya"

    print("creating pipeline...")
    pipeline = Pipeline(config, input_dir, output_dir)
    dag = pipeline.render()

    runner = DaskRunner()
    dsk, output = runner.create_dag(dag)
    # dot_graph(dsk, f"{Path(config).name.split('.')[0]}.png", rankdir="TB", collapse_outputs=True)

    print("creating output directories...")
    for directory in pipeline.directories.values():
        os.makedirs(directory, exist_ok=True)

    start = time.time()
    print("running dag...")
    runner = DaskRunner(scheduler=scheduler)
    if client is not None:
        runner.scheduler = client.get
        # runner.run(dag)
        if report:
            with performance_report(filename=filename):
                output = runner.run(dag, optimize=False)
        else:
            output = runner.run(dag, optimize=False)
        end = time.time()
        print(f"processing took {end - start:3.4f} seconds")
        # client.profile(filename='profile_client.html')  # save to html file
    else:
        output = runner.run(
            dag,
            optimize=True,
            ray_init_kwargs={
                "num_cpus": 35,
                "object_store_memory": 16 * 1e9,
                "dashboard_host": "0.0.0.0",
            },
        )

        # with Profiler() as prof, ResourceProfiler(dt=0.0001) as rprof, CacheProfiler() as cprof:
        # output = runner.run(dag, optimize=False)
        end = time.time()
        print(f"processing took {end - start:3.4f} seconds")
        # visualize([prof, rprof, cprof], filename=filename)

    print("SUCCESS!")


if __name__ == "__main__":

    local = False
    if local:
        client = None
        cluster = None
    else:
        from dask.distributed import LocalCluster, SubprocessCluster

        tpc = 1
        workers = 5
        cluster = LocalCluster(
            processes=True, n_workers=workers, threads_per_worker=tpc
        )  # Fully-featured local Dask cluster
        # cluster = SubprocessCluster()
        client = cluster.get_client()

    scheduler = "threads"
    if cluster:
        filename = f"client_{'processes'}_dask_c12-96_{workers}cpu_{tpc}tpc.html"
    else:
        filename = f"profile_{scheduler}_dask.html"
    test_run_pipeline(client, filename=filename, scheduler=scheduler, report=False)
