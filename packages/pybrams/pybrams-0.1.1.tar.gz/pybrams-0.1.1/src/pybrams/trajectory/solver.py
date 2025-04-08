import autograd.numpy as np

from tqdm import tqdm

from scipy.optimize import minimize, Bounds, NonlinearConstraint
from pybrams.utils.geometry import compute_fresnel_geometry
from pybrams.utils.kinematic import (
    compute_times_of_flight,
    compute_linear_velocity_profile,
)
from pybrams.utils import Config
from pybrams.utils.constants import TX_COORD, WAVELENGTH

from .solve_setup import (
    generate_initial_guesses,
    set_lower_solution_bounds,
    set_upper_solution_bounds,
    set_lower_ineq_constraint_bounds,
    set_upper_ineq_constraint_bounds,
    ineq_constraints,
)

import copy

from autograd import grad, jacobian
import logging

logger = logging.getLogger(__name__)


class Solver:

    def __init__(self, brams_data, args=None):

        if args:

            self.velocity_model = getattr(
                args, "velocity_model", Config.get(__name__, "default_velocity_model")
            )
            self.weight_pre_t0_objective = getattr(
                args,
                "weight_pre_t0_objective",
                Config.get(__name__, "default_weight_pre_t0_objective"),
            )
            self.outlier_removal = getattr(
                args, "outlier_removal", Config.get(__name__, "default_outlier_removal")
            )

        self.ref_system_code = None
        self.sorted_brams_data = None
        self.sort_brams_data(brams_data)
        self.format_inputs()
        self.set_ref_system()
        self.check_inputs()
        self.setup_solver()
        self.define_parameters()
        self.outlier_system_codes = []
        self.outlier_pre_t0_system_codes = []

    def solve(self):
        # Reconstruct a trajectory using BRAMS data

        self.converge_solution()
        self.output_solution()

    def sort_brams_data(self, brams_data):
        # Remove the system_codes which did not give a meteor t0

        for system_code, entry in brams_data.copy().items():

            meteor = entry["meteor"]

            if not meteor.t0:

                brams_data.pop(system_code)

        self.brams_data = brams_data
        self.sorted_brams_data = dict(
            sorted(self.brams_data.items(), key=lambda x: x[1]["meteor"].t0)
        )

    def format_inputs(self):
        # Format solver inputs from BRAMS outputs

        self.inputs = {}

        for system_code, entry in self.sorted_brams_data.items():

            if self.weight_pre_t0_objective == 0:

                t0 = entry["meteor"].t0_time_of_flight

            else:

                t0 = entry["meteor"].t0

            self.inputs[system_code] = {
                "coordinates": np.array(
                    [
                        entry["location"].coordinates.dourbocentric.x,
                        entry["location"].coordinates.dourbocentric.y,
                        entry["location"].coordinates.dourbocentric.z,
                    ]
                ),
                "t0": t0,
                "SNR": entry["meteor"].SNR,
                "sigma_t0": entry["meteor"].sigma_t0,
                "v_pseudo_pre_t0": entry["meteor"].v_pseudo_pre_t0,
                "r_value_pre_t0": entry["meteor"].r_value_pre_t0,
                "sigma_pre_t0": entry["meteor"].sigma_pre_t0,
            }

        self.initial_inputs = copy.deepcopy(self.inputs)

    def set_ref_system(self):
        # Determine the reference system which will be used for the computation of time of flights

        if self.weight_pre_t0_objective == 0:

            self.ref_system_code = min(
                self.inputs.items(), key=lambda item: item[1]["sigma_t0"]
            )[0]

        else:

            for system_code, entry in self.inputs.items():

                if (
                    entry.get("v_pseudo_pre_t0") is not None
                ):  # Check if field exists and is not None

                    self.ref_system_code = system_code
                    break  # Stop at the first valid system

        self.ref_t0 = self.inputs[self.ref_system_code]["t0"]
        self.ref_rx_coordinates = self.inputs[self.ref_system_code]["coordinates"]

    def check_inputs(self):

        self.inputs = {
            system_code: entry
            for system_code, entry in self.inputs.items()
            if abs(entry["t0"] - self.ref_t0)
            < Config.get(__name__, "maximum_time_of_flight")
        }

        if len(self.inputs) < Config.get(__name__, "minimum_number_systems"):

            raise ValueError(
                "Error occurred. Not enough BRAMS systems are exploitable."
            )

    def print_inputs(self):

        for system_code, entry in self.inputs.items():

            delta_t0 = entry["t0"] - self.ref_t0 if entry["t0"] is not None else None
            sigma_t0 = entry["sigma_t0"] if entry["sigma_t0"] is not None else None
            v_pseudo_pre_t0 = (
                entry["v_pseudo_pre_t0"]
                if entry["v_pseudo_pre_t0"] is not None
                else None
            )
            sigma_pre_t0 = (
                entry["sigma_pre_t0"] if entry["sigma_pre_t0"] is not None else None
            )

            logger.info(
                "%s - Time of flight [ms] = %s - Sigma t0 [ms] = %s - Pre-t0 pseudo speed [s⁻¹] = %s - Sigma pre-t0 [s⁻¹] = %s",
                system_code,
                np.round(1e3 * delta_t0, 2) if delta_t0 is not None else "N/A",
                np.round(1e3 * sigma_t0, 2) if sigma_t0 is not None else "N/A",
                np.round(v_pseudo_pre_t0, 2) if v_pseudo_pre_t0 is not None else "N/A",
                np.round(sigma_pre_t0, 2) if sigma_pre_t0 is not None else "N/A",
            )

    def setup_solver(self):

        self.system_codes = list(self.inputs.keys())
        self.ref_system_index = self.system_codes.index(self.ref_system_code)

        self.rx_coordinates = np.array(
            [
                system_code_dict["coordinates"]
                for system_code_dict in self.inputs.values()
            ]
        )

        self.times_of_flight = np.array(
            [
                (system_code_dict["t0"] - self.ref_t0)
                for system_code_dict in self.inputs.values()
            ]
        )

        self.max_times_of_flight = np.max(np.abs(self.times_of_flight))

        self.SNR = np.array(
            [system_code_dict["SNR"] for system_code_dict in self.inputs.values()]
        )

        self.sigma_times_of_flight = np.array(
            [
                np.sqrt(
                    system_code_dict["sigma_t0"] ** 2
                    + self.inputs[self.ref_system_code]["sigma_t0"] ** 2
                )
                for system_code_dict in self.inputs.values()
            ]
        )

        self.v_pseudo_pre_t0s = np.array(
            [
                system_code_dict["v_pseudo_pre_t0"]
                for system_code_dict in self.inputs.values()
                if system_code_dict["v_pseudo_pre_t0"]
            ]
        )

        self.system_codes_pre_t0s = [
            system_code
            for system_code, system_code_dict in self.inputs.items()
            if system_code_dict["v_pseudo_pre_t0"]
        ]

        self.rx_coordinates_pre_t0s = np.array(
            [
                system_code_dict["coordinates"]
                for system_code_dict in self.inputs.values()
                if system_code_dict["v_pseudo_pre_t0"]
            ]
        )

        self.sigma_pre_t0s = np.array(
            [
                system_code_dict["sigma_pre_t0"]
                for system_code_dict in self.inputs.values()
                if system_code_dict["v_pseudo_pre_t0"]
            ]
        )

    def define_parameters(self):

        self.variable_names = [
            "X [km]",
            "Y [km]",
            "Z [km]",
            "Vx [km/s]",
            "Vy [km/s]",
            "Vz [km/s]",
        ]

        if self.velocity_model == "linear":

            self.variable_names = np.concatenate(
                (self.variable_names, ["delta_t0 [s]", "a [km/s²]"])
            )

        self.output_names = [
            "\u03c6 [\u00b0]",
            "\u03b8 [\u00b0]",
            "Z₀ [km]",
            "V [km/s]",
        ]
        self.output_names = ["\u03c6 [°]", "\u03b8 [°]", "Z₀ [km]", "V [km/s]"]

    def converge_solution(self):
        # Solve the trajectory problem, excluding the system_codes with too high residuals

        self.solve = True

        while self.solve:

            self.call_solver()
            self.compute_residuals()

            if self.outlier_removal:

                self.remove_outliers()

    def compute_residuals(self):

        self.recon_times_of_flight = compute_times_of_flight(
            self.solution,
            TX_COORD,
            self.rx_coordinates,
            self.ref_rx_coordinates,
            self.velocity_model,
        )
        self.times_of_flight_residuals = (
            self.times_of_flight - self.recon_times_of_flight
        )

        start_coordinates = np.array(
            [self.solution[0], self.solution[1], self.solution[2]]
        )
        end_coordinates = np.array(
            [
                self.solution[0] + self.solution[3],
                self.solution[1] + self.solution[4],
                self.solution[2] + self.solution[5],
            ]
        )

        self.recon_K = compute_fresnel_geometry(
            start_coordinates, end_coordinates, TX_COORD, self.rx_coordinates_pre_t0s
        )
        self.recon_pre_t0_speeds = (
            self.recon_K * np.sqrt(WAVELENGTH / 2) * self.v_pseudo_pre_t0s
        )
        self.recon_speed_solution = np.sqrt(
            self.solution[3] ** 2 + self.solution[4] ** 2 + self.solution[5] ** 2
        )
        self.speeds_residuals = self.recon_pre_t0_speeds - self.recon_speed_solution

        median_times_of_flight_residuals = np.median(
            np.abs(self.times_of_flight_residuals)
        )
        rel_times_of_flight_residuals = (
            np.abs(self.times_of_flight_residuals - median_times_of_flight_residuals)
            / median_times_of_flight_residuals
        )
        self.max_rel_times_of_flight_residuals = np.max(rel_times_of_flight_residuals)

        self.rel_speeds_residuals = (
            self.recon_pre_t0_speeds - self.recon_speed_solution
        ) / self.recon_pre_t0_speeds
        median_speeds_residuals = np.median(np.abs(self.rel_speeds_residuals))
        rel_median_speeds_residuals = (
            np.abs(self.rel_speeds_residuals - median_speeds_residuals)
            / median_speeds_residuals
        )
        self.max_rel_speeds_residuals = np.max(rel_median_speeds_residuals)

        self.solve = False

        for i in range(len(self.system_codes)):
            logger.info(
                f"{self.system_codes[i]} - Time of flight residual [ms] = {np.round(1E3*self.times_of_flight_residuals[i])}"
            )

        for i in range(len(self.system_codes_pre_t0s)):
            logger.info(
                f"{self.system_codes_pre_t0s[i]} - Pre-t0 speed residual [%] = {np.round(1E2*self.rel_speeds_residuals[i])}"
            )

    def remove_outliers(self):
        # Remove outlier stations (too high pre-t0 speed residual or time of flight residual)

        speed_outlier = any(
            speed_residual > Config.get(__name__, "maximum_speed_residual")
            for speed_residual in abs(self.rel_speeds_residuals)
        )
        time_of_flight_outlier = any(
            time_of_flight_residual
            > Config.get(__name__, "maximum_times_of_flight_residual")
            for time_of_flight_residual in abs(self.times_of_flight_residuals)
        )
        speed_to_remove = (
            self.max_rel_speeds_residuals > self.max_rel_times_of_flight_residuals
        )

        if (
            (speed_outlier and time_of_flight_outlier and speed_to_remove)
            or (speed_outlier and not time_of_flight_outlier)
        ) and (self.weight_pre_t0_objective != 0):

            self.solve = True

            index_max_speed_residual = np.argmax(abs(self.rel_speeds_residuals))
            speed_outlier_system_code = self.system_codes_pre_t0s[
                index_max_speed_residual
            ]

            self.inputs[speed_outlier_system_code]["v_pseudo_pre_t0"] = None
            self.inputs[speed_outlier_system_code]["r_value_pre_t0"] = None

            self.outlier_pre_t0_system_codes.append(speed_outlier_system_code)

            self.inputs[speed_outlier_system_code]["t0"] = self.sorted_brams_data[
                speed_outlier_system_code
            ]["meteor"].t0_time_of_flight

            logger.info(f"Remove {speed_outlier_system_code} - too high speed residual")

        elif (speed_outlier and time_of_flight_outlier and not speed_to_remove) or (
            time_of_flight_outlier and not speed_outlier
        ):

            self.solve = True

            index_max_time_of_flight_residual = np.argmax(
                abs(self.times_of_flight_residuals)
            )
            time_of_flight_outlier_system_code = self.system_codes[
                index_max_time_of_flight_residual
            ]
            self.inputs.pop(time_of_flight_outlier_system_code)

            self.outlier_system_codes.append(time_of_flight_outlier_system_code)

            logger.info(
                f"Remove {time_of_flight_outlier_system_code} - too high time of flight residual "
            )

        if self.solve:

            self.set_ref_system()
            self.check_inputs()
            self.setup_solver()

            print("Solver restart after outlier removal")

            self.print_inputs()

    def remove_inputs(
        self, system_codes_to_remove=None, system_codes_to_remove_pre_t0s=None
    ):

        if system_codes_to_remove:
            for system_code in system_codes_to_remove:

                self.inputs.pop(system_code)
                self.outlier_system_codes.append(system_code)

        if system_codes_to_remove_pre_t0s:
            for system_code in system_codes_to_remove_pre_t0s:

                self.inputs[system_code]["v_pseudo_pre_t0"] = None
                self.inputs[system_code]["r_value_pre_t0"] = None
                self.outlier_pre_t0_system_codes.append(system_code)

        self.set_ref_system()
        self.check_inputs()
        self.setup_solver()

    def call_solver(self):
        # Call the trajectory solver with different initial guesses

        initial_guesses = generate_initial_guesses(self.velocity_model)

        lower_solution_bounds = set_lower_solution_bounds(self.velocity_model)
        upper_solution_bounds = set_upper_solution_bounds(self.velocity_model)
        self.solution_bounds = Bounds(lower_solution_bounds, upper_solution_bounds)

        lower_ineq_constraint_bounds = set_lower_ineq_constraint_bounds(self.inputs)
        upper_ineq_constraint_bounds = set_upper_ineq_constraint_bounds(self.inputs)

        self.solver_constraints = NonlinearConstraint(
            lambda x: ineq_constraints(x, self.rx_coordinates),
            lower_ineq_constraint_bounds,
            upper_ineq_constraint_bounds,
        )

        solutions = np.zeros(initial_guesses.shape)
        objective_values = 1e9 * np.ones(initial_guesses.shape[0])
        condition_numbers = np.zeros(initial_guesses.shape[0])
        hessians = [None] * initial_guesses.shape[0]

        hessian_fun = jacobian(grad(self.objective_fun))

        pbar = tqdm(position=0, total=initial_guesses.shape[0])

        for index, initial_guess in enumerate(initial_guesses):

            try:

                result = minimize(
                    self.objective_fun,
                    initial_guess,
                    method=Config.get(__name__, "optimization_method"),
                    bounds=self.solution_bounds,
                    constraints=self.solver_constraints,
                    tol=Config.get(__name__, "solver_tolerance"),
                    options={"disp": False},
                )
                solutions[index, :] = result.x
                objective_values[index] = result.fun
                hessians[index] = hessian_fun(result.x)

            except Exception:

                logger.info(f"Solving failed for initial guess {index}")

            pbar.update(1)

        index_solution = np.argmin(objective_values)

        self.condition_number = condition_numbers[index_solution]
        self.solution = solutions[index_solution, :]
        self.objective_value = objective_values[index_solution]
        self.hessian = hessians[index_solution]

    def posterior_fun(self, x):

        return -self.objective_fun(x) / 2

    def objective_fun(self, x):
        # Function to minimize by the nonlinear optimizer

        if self.weight_pre_t0_objective == 0:

            objective_fun = self.time_of_flight_fun(x)

        else:

            objective_fun = (
                1 - self.weight_pre_t0_objective
            ) * self.time_of_flight_fun(
                x
            ) + self.weight_pre_t0_objective * self.pre_t0_fun(
                x
            )

        return objective_fun

    def time_of_flight_fun(self, x):

        time_of_flight_residual = self.time_of_flight_residual(x)

        return np.sum(time_of_flight_residual**2)

    def pre_t0_fun(self, x):

        pre_t0_residual = self.pre_t0_residual(x)

        return np.sum(pre_t0_residual**2)

    def time_of_flight_residual(self, x):
        # Times of flight contribution to the objective

        iteration_times_of_flight = compute_times_of_flight(
            x,
            TX_COORD,
            self.rx_coordinates,
            self.ref_rx_coordinates,
            self.velocity_model,
        )

        time_of_flight_residual = (self.times_of_flight - iteration_times_of_flight) / (
            self.sigma_times_of_flight
        )

        return time_of_flight_residual

    def pre_t0_residual(self, x):
        # Pre-t0 speeds contribution to the objective

        start_coordinates = np.array([x[0], x[1], x[2]])
        end_coordinates = np.array([x[0] + x[3], x[1] + x[4], x[2] + x[5]])

        K = compute_fresnel_geometry(
            start_coordinates, end_coordinates, TX_COORD, self.rx_coordinates_pre_t0s
        )
        pre_t0_speeds = K * np.sqrt(WAVELENGTH / 2) * self.v_pseudo_pre_t0s

        if self.velocity_model == "constant":

            iteration_speed = np.sqrt(x[3] ** 2 + x[4] ** 2 + x[5] ** 2)
            iteration_speeds = iteration_speed * np.ones(len(self.v_pseudo_pre_t0s))

        elif self.velocity_model == "linear":

            linear_times_of_flight = compute_times_of_flight(
                x,
                TX_COORD,
                self.rx_coordinates_pre_t0s,
                self.ref_rx_coordinates,
                self.velocity_model,
            )
            iteration_speeds = compute_linear_velocity_profile(
                x, linear_times_of_flight
            )

        pre_t0_residual = (pre_t0_speeds - iteration_speeds) / (
            K * np.sqrt(WAVELENGTH / 2) * self.sigma_pre_t0s
        )

        return pre_t0_residual

    def is_within_bounds(self, x):

        return np.all(x >= self.solution_bounds.lb) and np.all(
            x <= self.solution_bounds.ub
        )

    def respects_constraints(self, x):

        constraint_value = self.solver_constraints.fun(x)

        # Check if the value is within the bounds
        return np.all(constraint_value >= self.solver_constraints.lb) and np.all(
            constraint_value <= self.solver_constraints.ub
        )

    def is_valid_fun(self, x):

        return self.is_within_bounds(x) and self.respects_constraints(x)

    def output_solution(self):

        self.number_inputs_time_of_flight = len(
            self.time_of_flight_residual(self.solution)
        )
        self.number_inputs_pre_t0 = len(self.pre_t0_residual(self.solution))
        self.number_inputs = self.number_inputs_time_of_flight

        if self.weight_pre_t0_objective != 0:
            self.number_inputs += self.number_inputs_pre_t0

        number_outputs = len(self.solution)
        self.number_dof = self.number_inputs - number_outputs
        residual_norm = self.objective_fun(self.solution)

        self.s_2 = residual_norm / (self.number_dof)

        logger.info("Solution")
        logger.info("X [km] = %.2f", np.round(self.solution[0], 2))
        logger.info("Y [km] = %.2f", np.round(self.solution[1], 2))
        logger.info("Z [km] = %.2f", np.round(self.solution[2], 2))
        logger.info("Vx [km/s] = %.2f", np.round(self.solution[3], 2))
        logger.info("Vy [km/s] = %.2f", np.round(self.solution[4], 2))
        logger.info("Vz [km/s] = %.2f", np.round(self.solution[5], 2))

        if self.velocity_model == "linear":

            logger.info("delta_t0 [s] = ", np.round(self.solution[6], 2))
            logger.info("a [km/s²] =", np.round(self.solution[7], 2))

        self.compute_covariance_matrix(self.hessian)

        self.target_time_of_flight = self.time_of_flight_fun(self.solution)
        self.target_pre_t0 = self.pre_t0_fun(self.solution)

    def compute_covariance_matrix(self, hessian):

        hessian_det = np.linalg.det(hessian)
        hessian_eig = np.linalg.eig(hessian)[0]
        self.hessian_cond = np.linalg.cond(hessian)

        logger.debug(f"Hessian determinant = {np.round(hessian_det, 2)}")
        logger.debug(f"Hessian eigenvalues = {np.round(hessian_eig, 2)}")

        logger.debug(f"Condition number = {np.round(self.hessian_cond, 2)}")

        self.cov = 2 * np.linalg.inv(hessian)
        self.sigma = np.sqrt(np.diag(self.cov))
        correlation_matrix = self.cov / np.outer(self.sigma, self.sigma)

        logger.debug(f"Standard deviation = {np.round(self.sigma, 2)}")
        logger.debug(f"Correlation matrix = ")
        logger.debug(np.round(correlation_matrix, 2))

        logger.debug("Confidence interval at 95%")

        self.confidence_interval = 1.96 * self.sigma

        for i in range(len(self.solution)):
            logger.debug(
                f"{self.variable_names[i]} = {np.round(self.solution[i], 2)} +- {np.round(self.confidence_interval[i], 2)}"
            )

    def update_cov_hessian(self, x):

        hessian_fun = jacobian(grad(self.objective_fun))
        self.hessian = hessian_fun(x)
        self.cov = 2 * np.linalg.inv(self.hessian)

    def to_dict(self):

        return self.__dict__

    def to_txt(self):

        text_lines = []

        for i in range(len(self.variable_names)):
            text_lines.append(
                f"Parameter {self.variable_names[i]} = {np.round(self.solution[i], 2)} - \u03c3 = {np.round(self.sigma[i], 2)}"
            )

        return "\n".join(text_lines)
