from canproc.pipelines import canesm_pipeline
from canproc.pipelines.utils import parse_formula
from canproc import register_module

# from dask.dot import dot_graph
from pathlib import Path
import pytest


data_folder = Path(__file__).parent.parent / "data"


@pytest.mark.parametrize(
    "formula, vars, ops",
    [
        ("FSO", ["FSO"], []),
        ("FSO+FSR", ["FSO", "FSR"], ["+"]),
        ("FSO-FSR+OLR", ["FSO", "FSR", "OLR"], ["-", "+"]),
        ("FSO/FSR-OLR", ["FSO", "FSR", "OLR"], ["/", "-"]),
        ("FSO*FSR/OLR", ["FSO", "FSR", "OLR"], ["*", "/"]),
        (" FSO *FSR/ OLR+BALT - BEG", ["FSO", "FSR", "OLR", "BALT", "BEG"], ["*", "/", "+", "-"]),
        ("TCD > CDBC", ["TCD", "CDBC"], [">"]),
        ("TCD >= CDBC", ["TCD", "CDBC"], [">="]),
        ("TCD < CDBC", ["TCD", "CDBC"], ["<"]),
        ("TCD <= CDBC", ["TCD", "CDBC"], ["<="]),
    ],
    ids=[
        "single",
        "short",
        "add-sub",
        "div-sub",
        "mul-div",
        "whitespace",
        "greater than",
        "greater than equal",
        "less than",
        "less than equal",
    ],
)
def test_formula_parsing(formula: str, vars: list[str], ops: list[str]):
    test_vars, test_ops = parse_formula(formula)
    assert test_vars == vars
    assert test_ops == ops


@pytest.mark.parametrize(
    "filename, num_ops",
    [
        ("canesm_pipeline.yaml", 93),
        ("canesm_pipeline_v52.yaml", 8),
        ("test_duplicate_output.yaml", 8),
        ("test_masked_variable.yaml", 8),
        ("test_xarray_ops.yaml", 10),
        ("test_formula.yaml", 23),
        ("test_formula_compute_syntax.yaml", 22),
        ("test_multistage_computation.yaml", 9),
        ("test_compute_and_dag_in_stage.yaml", 10),
        ("docs_example_pipeline.yaml", 19),
        ("test_stage_resample.yaml", 18),
        ("test_default_resample_freqs.yaml", 16),
        ("test_stage_cycle.yaml", 12),
        ("test_stage_area_mean.yaml", 10),
        ("test_compute_from_branch.yaml", 10),
    ],
    ids=[
        "canesm 6 pipeline",
        "canesm 5 pipeline",
        "duplicate outputs",
        "masked variable",
        "general xr dataset operations",
        "formula",
        "formula compute syntax",
        "multistage computation",
        "both compute and dag",
        "docs radiation example",
        "resample op in stage",
        "default resample stages",
        "cycle op in stage",
        "area_mean op in stage",
        "compute from branch",
    ],
)
def test_canesm_pipeline(filename: str, num_ops: int):
    """
    Test that the expected number of nodes are created.
    Note that this doesn't guarantee correctness and we should be testing
    node connections, but that is harder to check.
    """
    pipeline = data_folder / "pipelines" / filename
    dag = canesm_pipeline(pipeline, input_dir="test")
    assert len(dag.dag) == num_ops
    # assert dag.id[0 : len(dag_id)] == dag_id

    # runner = DaskRunner()
    # dsk, output = runner.create_dag(dag)
    # dot_graph(dsk, f"{filename.split('.')[0]}.png", rankdir="TB", collapse_outputs=True)


def test_metadata():
    pipeline = data_folder / "pipelines" / "test_metadata.yaml"
    dag = canesm_pipeline(pipeline, input_dir="test")
    assert dag.dag[3].kwargs["metadata"] == {
        "long_name": "Daily mean ground temperature aggregated over all tiles",
        "units": "K",
    }
    assert dag.dag[6].kwargs["metadata"] == {
        "long_name": "Monthly mean ground temperature aggregated over all tiles",
        "units": "K",
        "max": True,
        "min": True,
    }


def test_encoding_propagation():
    pipeline = data_folder / "pipelines" / "test_encoding.yaml"
    dag = canesm_pipeline(pipeline, input_dir="test")

    # test setup default (daily ST)
    assert dag.dag[3].kwargs["encoding"] == {"dtype": "float32", "_FillValue": 1.0e20}

    # test stage default (monthly ST)
    assert dag.dag[6].kwargs["encoding"] == {"dtype": "float64", "_FillValue": -999}

    # test variable encoding (monthly GT)
    assert dag.dag[10].kwargs["encoding"] == {"dtype": "float64", "_FillValue": 1.0e20}


def test_source_propagation():
    pipeline = data_folder / "pipelines" / "test_source.yaml"
    dag = canesm_pipeline(pipeline, input_dir="test")

    # test stage override (daily TAS)
    assert dag.dag[0].args[0] == "test/daily/TAS.nc"

    # test default source (monthly ST)
    assert dag.dag[4].args[0] == "test/*/ST.nc"

    # test variable override (monthly GT)
    assert dag.dag[8].args[0] == "test/_*_gs.001"


def test_pipeline_with_custom_function():

    # defined in conftest.py
    import mymodule

    register_module(mymodule, "mymodule")

    pipeline = data_folder / "pipelines" / "test_user_function.yaml"
    dag = canesm_pipeline(pipeline, input_dir="test")
    assert len(dag.dag) == 16
