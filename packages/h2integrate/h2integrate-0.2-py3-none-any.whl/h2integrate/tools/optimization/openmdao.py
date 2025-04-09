import numpy as np
import openmdao.api as om
from hopp.simulation import HoppInterface
from shapely.geometry import Point, Polygon

from h2integrate.simulation.h2integrate_simulation import (
    H2IntegrateSimulationConfig,
    run_simulation,
)


class H2IntegrateComponent(om.ExplicitComponent):
    """This class is an OpenMDAO wrapper for running a h2integrate simulation"""

    def initialize(self):
        self.options.declare(
            "config",
            types=H2IntegrateSimulationConfig,
            recordable=False,
            desc="H2IntegrateSimulationConfig data class instance",
        )
        self.options.declare(
            "outputs_for_finite_difference",
            default=["lcoh"],
            types=(type([""])),
            desc="outputs that should be finite differenced. Must be a list of str.",
        )
        self.options.declare(
            "turbine_x_init",
            types=(list, type(np.array(0))),
            desc="Initial turbine easting locations in m",
        )
        self.options.declare(
            "turbine_y_init",
            types=(list, type(np.array(0))),
            desc="Initial turbine northing locations in m",
        )
        self.options.declare(
            "verbose",
            default=False,
            types=bool,
            desc="Whether or not to print a bunch of stuff",
        )
        self.options.declare(
            "design_variables",
            # values=[
            #     "turbine_x",
            #     "turbine_y",
            #     "pv_capacity_kw",
            #     "wind_rating_kw",
            #     "electrolyzer_rating_kw",
            #     "battery_capacity_kw",
            #     "battery_capacity_kwh",
            # ],
            types=list,
            desc="List of design variables that should be included",
            default=[
                "pv_capacity_kw",
                "electrolyzer_rating_kw",
                "battery_capacity_kw",
                "battery_capacity_kwh",
            ],
            recordable=False,
        )

    def setup(self):
        ninputs = 0
        hopp_technologies = self.options["config"].hopp_config["technologies"]
        # Add inputs
        if "turbine_x" in self.options["design_variables"]:
            self.add_input("turbine_x", val=self.options["turbine_x_init"], units="m")
            ninputs += len(self.options["turbine_x_init"])
        if "turbine_y" in self.options["design_variables"]:
            self.add_input("turbine_y", val=self.options["turbine_y_init"], units="m")
            ninputs += len(self.options["turbine_y_init"])
        if "wind_rating_kw" in self.options["design_variables"]:
            initial_wind_rating = (
                hopp_technologies["wind"]["num_turbines"]
                * hopp_technologies["wind"]["turbine_rating_kw"]
            )
            self.add_input("wind_rating_kw", val=initial_wind_rating, units="kW")
            ninputs += 1
        if "pv_capacity_kw" in self.options["design_variables"]:
            self.add_input(
                "pv_capacity_kw",
                val=hopp_technologies["pv"]["system_capacity_kw"],
                units="kW",
            )
            ninputs += 1
        if "wave_capacity_kw" in self.options["design_variables"]:
            initial_wave_rating = (
                hopp_technologies["wave"]["device_rating_kw"]
                * hopp_technologies["wave"]["num_devices"]
            )
            self.add_input("wave_capacity_kw", val=initial_wave_rating, units="kW")
            ninputs += 1
        if "battery_capacity_kw" in self.options["design_variables"]:
            self.add_input(
                "battery_capacity_kw",
                val=hopp_technologies["battery"]["system_capacity_kw"],
                units="kW",
            )
            ninputs += 1
        if "battery_capacity_kwh" in self.options["design_variables"]:
            self.add_input(
                "battery_capacity_kwh",
                val=hopp_technologies["battery"]["system_capacity_kwh"],
                units="kW*h",
            )
            ninputs += 1
        if ninputs == 0 or "electrolyzer_rating_kw" in self.options["design_variables"]:
            self.add_input(
                "electrolyzer_rating_kw",
                val=self.options["config"].h2integrate_config["electrolyzer"]["rating"] * 1e3,
                units="kW",
            )
            ninputs += 1

        # add outputs
        self.add_output("lcoe", units="USD/(kW*h)", val=0.0, desc="levelized cost of energy")
        self.add_output("lcoh", units="USD/kg", val=0.0, desc="levelized cost of hydrogen")
        if "steel" in self.options["config"].h2integrate_config.keys():
            self.add_output("lcos", units="USD/t", val=0.0, desc="levelized cost of steel")
        if "ammonia" in self.options["config"].h2integrate_config.keys():
            self.add_output("lcoa", units="USD/kg", val=0.0, desc="levelized cost of ammonia")

        if self.options["config"].h2integrate_config["opt_options"]["constraints"][
            "pv_to_platform_area_ratio"
        ]["flag"]:
            self.add_output("pv_area", units="m*m", val=0.0, desc="offshore pv array area")
            self.add_output("platform_area", units="m*m", val=0.0, desc="offshore platform area")

            self.options["outputs_for_finite_difference"].append("pv_area")
            self.options["outputs_for_finite_difference"].append("platform_area")

    def compute(self, inputs, outputs):
        if self.options["verbose"]:
            print("reinitialize")

        config = self.options["config"]

        if any(
            x
            in [
                "wind_rating_kw",
                "pv_capacity_kw",
                "battery_capacity_kw",
                "battery_capacity_kwh",
            ]
            for x in inputs
        ):
            if "wind_rating_kw" in inputs:
                raise (
                    NotImplementedError(
                        "wind_rating_kw has not be fully implemented as a design variable"
                    )
                )
            if "pv_capacity_kw" in inputs:
                config.hopp_config["technologies"]["pv"]["system_capacity_kw"] = float(
                    inputs["pv_capacity_kw"]
                )
            if "battery_capacity_kw" in inputs:
                config.hopp_config["technologies"]["battery"]["system_capacity_kw"] = float(
                    inputs["battery_capacity_kw"]
                )
            if "battery_capacity_kwh" in inputs:
                config.hopp_config["technologies"]["battery"]["system_capacity_kwh"] = float(
                    inputs["battery_capacity_kwh"]
                )
        if "electrolyzer_rating_kw" in inputs:
            config.h2integrate_config["electrolyzer"]["rating"] = (
                float(inputs["electrolyzer_rating_kw"]) * 1e-3
            )

        if config.output_level == 0:
            run_simulation(config)
        elif config.output_level == 1:
            lcoh = run_simulation(config)
        elif config.output_level == 2:
            (
                lcoh,
                lcoe,
                capex_breakdown,
                opex_breakdown_annual,
                pf_lcoh,
                electrolyzer_physics_results,
            ) = run_simulation(config)
        elif config.output_level == 3:
            (
                lcoh,
                lcoe,
                capex_breakdown,
                opex_breakdown_annual,
                pf_lcoh,
                electrolyzer_physics_results,
                pf_lcoe,
                power_breakdown,
            ) = run_simulation(config)
        elif config.output_level == 4:
            lcoe, lcoh, lcoh_grid_only = run_simulation(config)
        elif config.output_level == 5:
            lcoe, lcoh, lcoh_grid_only, hopp_interface = run_simulation(config)
        elif config.output_level == 6:
            hopp_results, electrolyzer_physics_results, remaining_power_profile = run_simulation(
                config
            )
        elif config.output_level == 7:
            lcoe, lcoh, steel_finance, ammonia_finance = run_simulation(config)
        elif config.output_level == 8:
            h2integrate_output = run_simulation(config)
            lcoe = h2integrate_output.lcoe
            lcoh = h2integrate_output.lcoh
            steel_finance = h2integrate_output.steel_finance
            ammonia_finance = h2integrate_output.ammonia_finance
            pv_area = h2integrate_output.hopp_results["hybrid_plant"].pv.footprint_area
            platform_area = h2integrate_output.platform_results["toparea_m2"]

        outputs["lcoe"] = lcoe
        outputs["lcoh"] = lcoh

        if "steel" in self.options["config"].h2integrate_config.keys():
            outputs["lcos"] = steel_finance.sol.get("price")
        if "ammonia" in self.options["config"].h2integrate_config.keys():
            outputs["lcoa"] = ammonia_finance.sol.get("price")

        if self.options["config"].h2integrate_config["opt_options"]["constraints"][
            "pv_to_platform_area_ratio"
        ]["flag"]:
            outputs["pv_area"] = pv_area
            outputs["platform_area"] = platform_area

    def setup_partials(self):
        self.declare_partials(
            self.options["outputs_for_finite_difference"],
            "*",
            method="fd",
            form="forward",
        )


class HOPPComponent(om.ExplicitComponent):
    """This class is an OpenMDAO wrapper for running a HOPP simulation"""

    def initialize(self):
        self.options.declare(
            "hi",
            types=HoppInterface,
            recordable=False,
            desc="HOPP Interface class instance",
        )
        self.options.declare(
            "turbine_x_init",
            types=(list, type(np.array(0))),
            desc="Initial turbine easting locations in m",
        )
        self.options.declare(
            "turbine_y_init",
            types=(list, type(np.array(0))),
            desc="Initial turbine northing locations in m",
        )
        self.options.declare(
            "verbose",
            default=False,
            types=bool,
            desc="Whether or not to print a bunch of stuff",
        )
        self.options.declare(
            "design_variables",
            # values=[
            #     "turbine_x",
            #     "turbine_y",
            #     "pv_capacity_kw",
            #     "wind_rating_kw",
            #     "electrolyzer_rating_kw",
            #     "battery_capacity_kw",
            #     "battery_capacity_kwh",
            # ],
            types=list,
            desc="List of design variables that should be included",
            default=["turbine_x", "turbine_y"],
            recordable=False,
        )

    def setup(self):
        ninputs = 0
        if "turbine_x" in self.options["design_variables"]:
            self.add_input("turbine_x", val=self.options["turbine_x_init"], units="m")
            ninputs += len(self.options["turbine_x_init"])
        if "turbine_y" in self.options["design_variables"]:
            self.add_input("turbine_y", val=self.options["turbine_y_init"], units="m")
            ninputs += len(self.options["turbine_y_init"])
        if "wind_rating_kw" in self.options["design_variables"]:
            self.add_input("wind_rating_kw", val=150000, units="kW")
            ninputs += 1
        if "pv_capacity_kw" in self.options["design_variables"]:
            self.add_input("pv_capacity_kw", val=15000, units="kW")
            ninputs += 1
        if "battery_capacity_kw" in self.options["design_variables"]:
            self.add_input("battery_capacity_kw", val=15000, units="kW")
            ninputs += 1
        if "battery_capacity_kwh" in self.options["design_variables"]:
            self.add_input("battery_capacity_kwh", val=15000, units="kW*h")
            ninputs += 1
        if ninputs == 0:
            self.add_input("turbine_x", val=self.options["turbine_x_init"], units="m")

        technologies = self.options["hi"].configuration["technologies"]

        if "pv" in technologies.keys():
            self.add_output("pv_capex", val=0.0, units="USD")
            # self.add_output("pv_opex", val=0.0, units="USD")
        if "wind" in technologies.keys():
            self.add_output("wind_capex", val=0.0, units="USD")
            # self.add_output("wind_opex", val=0.0, units="USD")
        if "battery" in technologies.keys():
            self.add_output("battery_capex", val=0.0, units="USD")
            # self.add_output("battery_opex", val=0.0, units="USD")

        self.add_output("hybrid_electrical_generation_capex", units="USD")
        self.add_output("hybrid_electrical_generation_opex", units="USD")
        self.add_output("aep", units="kW*h")
        self.add_output("lcoe_real", units="USD/(kW*h)")
        self.add_output("power_signal", units="kW", val=np.zeros(8760))

    def compute(self, inputs, outputs):
        hi = self.options["hi"]
        technologies = hi.configuration["technologies"]

        if any(
            x
            in [
                "wind_rating_kw",
                "pv_capacity_kw",
                "battery_capacity_kw",
                "battery_capacity_kwh",
            ]
            for x in inputs
        ):
            if "wind_rating_kw" in inputs:
                raise (
                    NotImplementedError(
                        "wind_rating_kw has not be fully implemented as a design variable"
                    )
                )
            if "pv_capacity_kw" in inputs:
                technologies["pv"]["system_capacity_kw"] = float(inputs["pv_capacity_kw"])
            if "battery_capacity_kw" in inputs:
                technologies["battery"]["system_capacity_kw"] = float(inputs["battery_capacity_kw"])
            if "battery_capacity_kwh" in inputs:
                technologies["battery"]["system_capacity_kwh"] = float(
                    inputs["battery_capacity_kwh"]
                )

            configuration = hi.configuration
            configuration["technologies"] = technologies
            hi.reinitialize(configuration)

        if ("turbine_x" in inputs) or ("turbine_y" in inputs):
            if "turbine_x" not in inputs:
                hi.system.wind._system_model.fi.set(layout_y=inputs["turbine_y"])
            elif "turbine_y" not in inputs:
                hi.system.wind._system_model.fi.set(layout_x=inputs["turbine_x"])
            else:
                hi.system.wind._system_model.fi.set(
                    layout_x=inputs["turbine_x"], layout_y=inputs["turbine_y"]
                )

        # run simulation
        hi.simulate(25)

        if self.options["verbose"]:
            print(f"obj: {hi.system.annual_energies.hybrid}")

        # get results
        if "pv" in technologies.keys():
            outputs["pv_capex"] = hi.system.pv.total_installed_cost
            # outputs["pv_opex"] = hi.system.pv.om_total_expense[1]
        if "wind" in technologies.keys():
            outputs["wind_capex"] = hi.system.wind.total_installed_cost
            # outputs["wind_opex"] = hi.system.wind.om_total_expense[1]
        if "battery" in technologies.keys():
            outputs["battery_capex"] = hi.system.battery.total_installed_cost
            # outputs["battery_opex"] = hi.system.battery.om_total_expense[1]

        outputs["hybrid_electrical_generation_capex"] = hi.system.cost_installed["hybrid"]
        # outputs["hybrid_electrical_generation_opex"] = hi.system.om_total_expenses[1]

        outputs["aep"] = hi.system.annual_energies.hybrid
        outputs["lcoe_real"] = (
            hi.system.lcoe_real.hybrid / 100.0
        )  # convert from cents/kWh to USD/kWh
        outputs["power_signal"] = hi.system.grid.generation_profile[0:8760]

    def setup_partials(self):
        self.declare_partials(["lcoe_real", "power_signal"], "*", method="fd", form="forward")


class TurbineDistanceComponent(om.ExplicitComponent):
    """This class is an OpenMDAO component for placing a constraint on wind turbine distances"""

    def initialize(self):
        self.options.declare("turbine_x_init")
        self.options.declare("turbine_y_init")

    def setup(self):
        n_turbines = len(self.options["turbine_x_init"])
        n_distances = int(n_turbines * (n_turbines - 1) / 2)
        self.add_input("turbine_x", val=self.options["turbine_x_init"], units="m")
        self.add_input("turbine_y", val=self.options["turbine_y_init"], units="m")
        self.add_output("spacing_vec", val=np.zeros(n_distances), units="m")

    def compute(self, inputs, outputs):
        n_turbines = len(inputs["turbine_x"])
        spacing_vec = np.zeros(int(n_turbines * (n_turbines - 1) / 2))
        k = 0
        for i in range(len(inputs["turbine_x"])):
            for j in range(i + 1, len(inputs["turbine_y"])):  # only look at pairs once
                spacing_vec[k] = np.linalg.norm(
                    [
                        (inputs["turbine_x"][i] - inputs["turbine_x"][j]),
                        (inputs["turbine_y"][i] - inputs["turbine_y"][j]),
                    ]
                )
                k += 1
        outputs["spacing_vec"] = spacing_vec

    def setup_partials(self):
        self.declare_partials("*", "*", method="fd", form="forward")


class BoundaryDistanceComponent(om.ExplicitComponent):
    """This class is an OpenMDAO component for placing a boundary constraint on wind turbine
    locations.
    """

    def initialize(self):
        self.options.declare("hopp_interface", recordable=False)
        self.options.declare("turbine_x_init")
        self.options.declare("turbine_y_init")

    def setup(self):
        self.n_turbines = len(self.options["turbine_x_init"])
        self.n_distances = self.n_turbines
        self.add_input("turbine_x", val=self.options["turbine_x_init"], units="m")
        self.add_input("turbine_y", val=self.options["turbine_y_init"], units="m")
        self.add_output("boundary_distance_vec", val=np.zeros(self.n_distances), units="m")

    def compute(self, inputs, outputs):
        # get hopp interface
        hi = self.options["hopp_interface"]

        # get polygon for boundary
        boundary_polygon = Polygon(hi.system.site.vertices)

        # check if turbines are inside polygon and get distance
        for i in range(0, self.n_distances):
            point = Point(inputs["turbine_x"][i], inputs["turbine_y"][i])
            outputs["boundary_distance_vec"][i] = boundary_polygon.exterior.distance(point)
            if not boundary_polygon.contains(point):
                outputs["boundary_distance_vec"][i] *= -1

    def setup_partials(self):
        self.declare_partials("*", "*", method="fd", form="forward")
