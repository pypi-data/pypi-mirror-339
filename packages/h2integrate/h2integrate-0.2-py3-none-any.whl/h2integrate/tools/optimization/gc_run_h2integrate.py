"""
This file is based on the WISDEM file 'runWISDEM.py`: https://github.com/WISDEM/WISDEM
"""

import sys
import logging
from pathlib import Path

import numpy as np

from h2integrate.tools.optimization import fileIO
from h2integrate.tools.optimization.openmdao import H2IntegrateComponent
from h2integrate.tools.optimization.mpi_tools import MPI, map_comm_heirarchical
from h2integrate.simulation.h2integrate_simulation import (
    H2IntegrateSimulationConfig,
    setup_simulation,
)
from h2integrate.tools.optimization.gc_PoseOptimization import PoseOptimization


def run_h2integrate(config: H2IntegrateSimulationConfig, overridden_values=None, run_only=False):
    """This functions sets up and runs h2integrate. It can be used for analysis runs, optimizations,
    design of experiments, or step size studies

    Args:
        config (H2IntegrateSimulationConfig): data structure class containing all simulation options
        overridden_values (_type_, optional): data values from `config` may be overridden using this
            input at call time. Defaults to None.
        run_only (bool, optional): if True, not optimization or design of experiments will be run.
            Defaults to False.

    Returns:
        prob: an openmdao problem instance
        config: see Args
    """
    # Initialize openmdao problem. If running with multiple processors in MPI, use parallel finite
    # differencing equal to the number of cores used.
    # Otherwise, initialize the H2Integrate system normally. Get the rank number for
    # parallelization.
    # We only print output files using the root processor.
    myopt = PoseOptimization(config)

    if MPI:
        n_DV = myopt.get_number_design_variables()

        # Extract the number of cores available
        max_cores = MPI.COMM_WORLD.Get_size()

        if (
            max_cores > n_DV
            and not config.h2integrate_config["opt_options"]["driver"]["design_of_experiments"][
                "flag"
            ]
        ):
            raise ValueError(
                "ERROR: please reduce the number of cores, currently set to "
                + str(max_cores)
                + ", to the number of finite differences "
                + str(n_DV)
                + ", which is equal to the number of design variables DV for forward differencing"
                + " and DV times 2 for central differencing,"
                + " or the parallelization logic will not work"
            )

        if config.h2integrate_config["opt_options"]["driver"]["design_of_experiments"]["flag"]:
            n_FD = max_cores

        else:
            # Define the color map for the parallelization, determining the maximum number of
            # parallel finite difference (FD) evaluations based on the number of design variables
            # (DV).
            n_FD = min([max_cores, n_DV])

            # Define the color map for the cores
            n_FD = max([n_FD, 1])

        comm_map_down, comm_map_up, color_map = map_comm_heirarchical(n_FD, 1)
        rank = MPI.COMM_WORLD.Get_rank()
        color_i = color_map[rank]
        comm_i = MPI.COMM_WORLD.Split(color_i, 1)
    else:
        color_i = 0
        rank = 0

    folder_output = Path(config.output_dir).resolve()

    if "opt_options" in config.h2integrate_config.keys():
        design_variables = [
            key
            for key in [*config.h2integrate_config["opt_options"]["design_variables"]]
            if config.h2integrate_config["opt_options"]["design_variables"][key]["flag"]
        ]
    else:
        design_variables = []

    if rank == 0 and "opt_options" in config.h2integrate_config.keys():
        folder_output.mkdir(exist_ok=True)

        # create logger
        logger = logging.getLogger("h2integrate")
        logger.setLevel(logging.INFO)

        # create handlers
        ht = logging.StreamHandler()
        ht.setLevel(logging.WARNING)

        flog = (
            folder_output
            / f'{config.h2integrate_config["opt_options"]["general"]["fname_output"]}.log'
        )
        hf = logging.FileHandler(flog, mode="w")
        hf.setLevel(logging.INFO)

        # create formatters
        formatter_t = logging.Formatter(
            "%(module)s:%(funcName)s:%(lineno)d %(levelname)s:%(message)s"
        )
        formatter_f = logging.Formatter(
            "P%(process)d %(asctime)s %(module)s:%(funcName)s:%(lineno)d %(levelname)s:%(message)s"
        )

        # add formatter to handlers
        ht.setFormatter(formatter_t)
        hf.setFormatter(formatter_f)

        # add handlers to logger
        logger.addHandler(ht)
        logger.addHandler(hf)
        logger.info("Started")

    if color_i == 0:  # the top layer of cores enters
        import openmdao.api as om

        if MPI:
            # Parallel settings for OpenMDAO
            prob = om.Problem(model=om.Group(num_par_fd=n_FD), comm=comm_i, reports=False)

        else:
            # Sequential finite differencing
            prob = om.Problem(model=om.Group(), reports=False)

        prob.model.add_subsystem(
            "h2integrate",
            H2IntegrateComponent(config=config, design_variables=design_variables),
            promotes=["*"],
        )

        # If at least one of the design variables is active, setup an optimization
        if not run_only and config.h2integrate_config["opt_options"]["opt_flag"]:
            config, hi, _ = setup_simulation(config)
            prob = myopt.set_driver(prob)
            prob = myopt.set_objective(prob)
            prob = myopt.set_design_variables(prob, config, hi)
            prob = myopt.set_constraints(prob, hi)

        if config.h2integrate_config["opt_options"]["recorder"]["flag"]:
            prob = myopt.set_recorders(prob)

        # Setup openmdao problem
        prob.setup()

        # If the user provides values in this dict, they overwrite
        # whatever values have been set by the yaml files.
        # This is useful for performing black-box wrapped optimization without
        # needing to modify the yaml files.
        if overridden_values is not None:
            for key in overridden_values:
                prob[key] = overridden_values[key]

        # Place the last design variables from a previous run into the problem.
        # This needs to occur after the above setup() and yaml2openmdao() calls
        # so these values are correctly placed in the problem.

        if not run_only:
            prob = myopt.set_restart(prob)

            if "check_totals" in config.h2integrate_config["opt_options"]["driver"]:
                if config.h2integrate_config["opt_options"]["driver"]["check_totals"]:
                    prob.run_model()
                    prob.compute_totals()

            if "check_partials" in config.h2integrate_config["opt_options"]["driver"]:
                if config.h2integrate_config["opt_options"]["driver"]["check_partials"]:
                    prob.run_model()
                    prob.check_partials(compact_print=True)

            sys.stdout.flush()

            if config.h2integrate_config["opt_options"]["driver"]["step_size_study"]["flag"]:
                prob.run_model()
                study_options = config.h2integrate_config["opt_options"]["driver"][
                    "step_size_study"
                ]
                step_sizes = study_options["step_sizes"]
                all_derivs = {}
                for idx, step_size in enumerate(step_sizes):
                    prob.model.approx_totals(
                        method="fd", step=step_size, form=study_options["form"]
                    )

                    if study_options["of"]:
                        of = study_options["of"]
                    else:
                        of = None

                    if study_options["wrt"]:
                        wrt = study_options["wrt"]
                    else:
                        wrt = None

                    derivs = prob.compute_totals(
                        of=of, wrt=wrt, driver_scaling=study_options["driver_scaling"]
                    )
                    all_derivs[idx] = derivs
                    all_derivs[idx]["step_size"] = step_size
                np.save("total_derivs.npy", all_derivs)

            # Run openmdao problem
            elif config.h2integrate_config["opt_options"]["opt_flag"]:
                prob.run_driver()
        else:
            prob.run_model()
        if config.h2integrate_config["opt_options"]["recorder"]["flag"]:
            prob.record("final_state")

        if (not MPI) or (MPI and rank == 0):
            # Save data coming from openmdao to an output yaml file
            froot_out = (
                folder_output / config.h2integrate_config["opt_options"]["general"]["fname_output"]
            )

            # Save data to numpy and matlab arrays
            fileIO.save_data(froot_out, prob)

    if rank == 0:
        return prob, config
    else:
        return [], []
