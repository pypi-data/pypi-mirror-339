from pathlib import Path

import openmdao.api as om

from h2integrate.simulation.h2integrate_simulation import H2IntegrateSimulationConfig
from h2integrate.tools.optimization.gc_run_h2integrate import run_h2integrate


ROOT_DIR = Path(__file__).parents[2]

solar_resource_file = (
    ROOT_DIR / "resource_files" / "solar" / "35.2018863_-101.945027_psmv3_60_2012.csv"
)
wind_resource_file = (
    ROOT_DIR
    / "resource_files"
    / "wind"
    / "35.2018863_-101.945027_windtoolkit_2012_60min_80m_100m.srw"
)
floris_input_filename = Path(__file__).absolute().parent / "inputs" / "floris_input.yaml"
hopp_config_filename = (
    Path(__file__).absolute().parent
    / "input_files"
    / "plant"
    / "hopp_config_wind_wave_solar_battery.yaml"
)
h2integrate_config_filename = (
    Path(__file__).absolute().parent / "input_files" / "plant" / "h2integrate_config.yaml"
)
turbine_config_filename = (
    Path(__file__).absolute().parent / "input_files" / "turbines" / "osw_18MW.yaml"
)
rtol = 1e-5


def setup_h2integrate():
    config = H2IntegrateSimulationConfig(
        filename_hopp_config=hopp_config_filename,
        filename_h2integrate_config=h2integrate_config_filename,
        filename_turbine_config=turbine_config_filename,
        filename_floris_config=floris_input_filename,
        verbose=False,
        show_plots=False,
        save_plots=False,
        output_dir=str(Path(__file__).absolute().parent / "output"),
        use_profast=True,
        post_processing=False,
        incentive_option=1,
        plant_design_scenario=9,
        output_level=7,
    )

    # based on 2023 ATB moderate case for onshore wind
    config.hopp_config["config"]["cost_info"]["wind_installed_cost_mw"] = 1434000.0
    # based on 2023 ATB moderate case for onshore wind
    config.hopp_config["config"]["cost_info"]["wind_om_per_kw"] = 29.567
    config.hopp_config["technologies"]["wind"]["fin_model"]["system_costs"]["om_fixed"][0] = (
        config.hopp_config["config"]["cost_info"]["wind_om_per_kw"]
    )
    # set skip_financial to false for onshore wind
    config.hopp_config["config"]["simulation_options"]["wind"]["skip_financial"] = False

    config.h2integrate_config["opt_options"] = {
        "opt_flag": True,
        "general": {
            "folder_output": "output",
            "fname_output": "test_run_h2integrate_optimization_mpi",
        },
        "design_variables": {
            "electrolyzer_rating_kw": {
                "flag": True,
                "lower": 10000.0,
                "upper": 200000.0,
                "units": "kW",
            },
            "pv_capacity_kw": {
                "flag": True,
                "lower": 1000.0,
                "upper": 1500000.0,
                "units": "kW",
            },
            "wave_capacity_kw": {
                "flag": False,
                "lower": 1000.0,
                "upper": 1500000.0,
                "units": "kW",
            },
            "battery_capacity_kw": {
                "flag": False,
                "lower": 1000.0,
                "upper": 1500000.0,
                "units": "kW",
            },
            "battery_capacity_kwh": {
                "flag": False,
                "lower": 1000.0,
                "upper": 1500000.0,
                "units": "kW*h",
            },
            "turbine_x": {
                "flag": False,
                "lower": 0.0,
                "upper": 1500000.0,
                "units": "m",
            },
            "turbine_y": {
                "flag": False,
                "lower": 0.0,
                "upper": 1500000.0,
                "units": "m",
            },
        },
        "constraints": {
            "turbine_spacing": {
                "flag": False,
                "lower": 0.0,
            },
            "boundary_distance": {
                "flag": False,
                "lower": 0.0,
            },
            "pv_to_platform_area_ratio": {
                "flag": False,
                "upper": 1.0,  # relative size of solar pv area to platform area
            },
            "user": {},
        },
        "merit_figure": "lcoh",
        "merit_figure_user": {
            "name": "lcoh",
            "max_flag": False,
            "ref": 1.0,  # value of objective that scales to 1.0
        },
        "driver": {
            "optimization": {
                "flag": True,
                "solver": "SLSQP",
                "tol": 1e-6,
                "max_major_iter": 1,
                "max_minor_iter": 2,
                "gradient_method": "openmdao",
                # "time_limit": 10, # (sec) optional
                # "hist_file_name": "snopt_history.txt", # optional
                "verify_level": -1,  # optional
                "step_calc": None,
                # Type of finite differences to use, one of ["forward", "backward", "central"]
                "form": "forward",
                "debug_print": False,
            },
            "design_of_experiments": {
                "flag": False,
                "run_parallel": False,
                # [Uniform, FullFact, PlackettBurman, BoxBehnken, LatinHypercube]
                "generator": "FullFact",
                # Number of samples to evaluate model at (Uniform and LatinHypercube only)
                "num_samples": 1,
                "seed": 2,
                #  Number of evenly spaced levels between each design variable lower and
                # upper bound (FullFactorial only)
                "levels": 50,
                # [None, center, c, maximin, m, centermaximin, cm, correelation, corr]
                "criterion": None,
                "iterations": 1,
                "debug_print": False,
            },
            "step_size_study": {"flag": False},
        },
        "recorder": {
            "flag": True,
            "file_name": str(Path(__file__).absolute().parent / "output" / "recorder.sql"),
            "includes": False,
        },
    }

    return config


# @pytest.mark.mpi
def test_run_h2integrate_optimize_mpi(subtests):
    try:
        from mpi4py import MPI

        is_mpi = True
    except ModuleNotFoundError:
        is_mpi = False

    config = setup_h2integrate()

    prob, config = run_h2integrate(config, run_only=False)

    if is_mpi:
        rank = MPI.COMM_WORLD.Get_rank()
    else:
        rank = 0

    if rank == 0:
        cr = om.CaseReader(Path(__file__).absolute().parent / "output" / "recorder.sql")

        # get initial LCOH
        case = cr.get_case(0)
        lcoh_init = case.get_val("lcoh", units="USD/kg")[0]

        # get final LCOH
        case = cr.get_case(-1)
        lcoh_final = case.get_val("lcoh", units="USD/kg")[0]

        with subtests.test("lcoh"):
            assert lcoh_final <= lcoh_init
