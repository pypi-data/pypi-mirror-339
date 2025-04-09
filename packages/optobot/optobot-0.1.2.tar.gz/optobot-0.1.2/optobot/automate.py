import datetime
import os
import string
import sys

import numpy as np
import pandas as pd

from optobot.optimisation import optimisers
from optobot.ot2_protocol import generate_script

"""
image-file storing only worked when run from powershell - fix
include error threshold to stop run
fix different nr of population_size
store and import previous optimisation data (to not have to repeat runs)

"""


class OptimisationLoop:
    """
    A class to use the 96 well plate with optimisation algorithms.

    Parameters:
        - objective_function (function):
            Function to calculate the error based the measured values obtained after using certain liquid-volumes in the experiment.
        - exp_data_dir (string):
            directory to store the experimental data.
        - wellplate_shape (tuple):
            tuple representing the shape (rows, columns) of the wellplate.
        - population_size (int):
            Number of wells used in each (optimization) iteration
        - measurement_function (bool):
            boolean indicating whether the measured values should be manually added to the "measurements" csv file, or whether instead
            the "measure_colors" function should be called.
        - liquid_names (list of strings):
            list of the names of the liquids used in the experiment.
        - measured_parameter_names (list of strings):
            list of the names of the elements of one measurement (e.g. "red, "green" and "blue" of RBG values)
        - wellplate_locs (list of ints):
            list containing the location of the wellplate(s) that want to be used.
        - total_volume:
            Total liquid volume per well.

    """

    def __init__(
        self,
        objective_function,
        liquid_names,
        measured_parameter_names,
        target_measurement,
        relative_tolerance=0.05,
        population_size=12,
        name="experiment",
        measurement_function="manual",
        wellplate_shape=[8, 12],
        wellplate_locs=[5],
        total_volume=90.0,
    ):

        self.objective_function = objective_function

        # Create experiment directory. All the data will be saved here.
        current_datetime = datetime.datetime.now().strftime("%a-%d-%b-%Y-at-%I-%M-%S%p")
        exp_id = f"{name}_{current_datetime}"
        os.makedirs(exp_id, exist_ok=True)
        self.exp_data_dir = exp_id

        self.wellplate_shape = wellplate_shape
        self.iteration_count = 0  # Initialize iteration counter
        self.num_liquids = len(liquid_names)
        self.measured_parameter_names = measured_parameter_names
        self.num_measured_parameters = len(measured_parameter_names)
        self.population_size = population_size
        self.liquid_names = liquid_names
        self.measurement_function = measurement_function
        self.wellplate_locs = wellplate_locs
        self.num_wellplates = len(wellplate_locs)
        self.total_volume = total_volume
        self.blank_row_space = 1  # vertical space between wellplate data in CSV files (if more than one is used)
        self.target_measurement = np.array(target_measurement)
        self.relative_tolerance = relative_tolerance

        # Initialize dataframes for storing experimental data
        self.liquid_volume_df, self.measurements_df, self.error_df, self.all_data_df = (
            self.init_dataframes()
        )

    def __call__(self, liquid_volumes):
        """
        Executes one optimization iteration.
        1. Takes the input volumes of each liquid and calculates how much water to use to dilute each set.
        2. generates the opentrons-run script for this iteration,
        3. Waits for the user to upload this script to the robot,
        4. Gathers the measurements (e.g. final colors if dyes are mixed) after the liquids have been combined in each well - either manually or by calling a measurement function,
        5. Computes the errors by calling the objective function that compares these measurements to an ideal, pre-defined measurement.

        Parameters:
        - liquid_volumes (ndarray):
            Array containing the volumes of each liquid that will be put in each of the wells of the current iteration.
            Its shape is (population_size, num_liquids).

        Returns:
        - errors (array):
            Computed errors from the objective function.

        """

        # Adds water so that it fills up to the same volume each time
        water_vol = self.total_volume - np.sum(liquid_volumes, axis=1)
        # water will now be the first liquid to be added
        liquid_volumes = np.hstack([water_vol.reshape(-1, 1), liquid_volumes])

        # path where the generated script will be stored
        filepath = f"{self.exp_data_dir}/generated_ot2_script.py"
        generate_script(
            filepath,
            self.iteration_count,
            self.population_size,
            liquid_volumes,
            self.wellplate_locs,
        )

        input("Upload script, wait for robot, and then press any key to continue: ")

        # obtain measurements either manually or automatically (in the case that color-recording wants to be done)
        if self.measurement_function == "manual":
            measurements = self.user_input()
        else:
            # measurements = self.measure_colors()
            measurements = self.measurement_function(
                liquid_volumes,
                self.iteration_count,
                self.population_size,
                self.num_measured_parameters,
                self.exp_data_dir,
            )

        errors = self.objective_function(measurements)

        # Data storage
        self.store_data(liquid_volumes, measurements, errors)


        if self.target_measurement is not None: 
            # Terminate the optimisation loop if the measurements are close enough to the target measurement,
            # based on the specified relative tolerance
            self.check_convergence(measurements)

        # update the iteration count
        self.iteration_count += 1

        return errors

    def init_dataframes(self):
        """
        Initializes dataframes for liquid volumes, measurements, errors, and a dataframe where all data appear together.
        """

        wellplate_nr_rows = self.wellplate_shape[0]
        wellplate_nr_columns = self.wellplate_shape[1]

        # constructs the letter-index for the wellplate-shaped csvs,
        # taking into account the vertical spacing for when the data of multiple wellplates wants to be stored.
        wellplate_index = []
        for i in range(self.num_wellplates):

            # e.g., [A, B, C, D, E, F, G, H]
            wellplate_rows = [
                string.ascii_uppercase[i % 26] for i in range(wellplate_nr_rows)
            ]

            if i != self.num_wellplates - 1:
                wellplate_index.extend(wellplate_rows + [""] * self.blank_row_space)
            else:
                wellplate_index.extend(wellplate_rows)

        # define column indices
        liquid_columns = pd.MultiIndex.from_product(
            [np.arange(1, wellplate_nr_columns + 1), self.liquid_names]
        )
        measurement_columns = pd.MultiIndex.from_product(
            [np.arange(1, wellplate_nr_columns + 1), self.measured_parameter_names]
        )
        error_columns = np.arange(1, wellplate_nr_columns + 1)
        all_data_columns = (
            ["iteration_number"]
            + [f"vol_{liquid_name}" for liquid_name in self.liquid_names]
            + self.measured_parameter_names
            + ["error"]
        )

        total_rows = self.num_wellplates * wellplate_nr_rows + (
            self.blank_row_space * (self.num_wellplates - 1)
        )

        def create_csv(filename, shape, index=None, columns=None):
            filepath = f"{self.exp_data_dir}/{filename}.csv"

            df = pd.DataFrame(data=np.zeros(shape), index=index, columns=columns)
            df.to_csv(filepath)
            return df

        # creates and saved the empty csvs to the experiment folder
        liquid_volume_df = create_csv(
            "liquid_volumes",
            (total_rows, wellplate_nr_columns * self.num_liquids),
            wellplate_index,
            liquid_columns,
        )
        errors_df = create_csv(
            "errors", (total_rows, wellplate_nr_columns), wellplate_index, error_columns
        )
        measurements_df = create_csv(
            "measurements",
            (total_rows, wellplate_nr_columns * self.num_measured_parameters),
            wellplate_index,
            measurement_columns,
        )
        all_data_df = create_csv(
            "all_data",
            (
                self.num_wellplates * wellplate_nr_rows * wellplate_nr_columns,
                len(all_data_columns),
            ),
            columns=all_data_columns,
        )

        return liquid_volume_df, measurements_df, errors_df, all_data_df

    def store_data(self, liquid_volumes, measurements, errors):
        """
        Stores the data for the current iteration in csv files (which will also hold the data for the subsequent iterations of the experiment.)

        """
        total_wells = self.wellplate_shape[0] * self.wellplate_shape[1]
        raw_start_index = self.iteration_count * self.population_size
        current_well_plate = raw_start_index // total_wells

        # The start and end-indexes will be used on the flattened dataframes (in the case of volumes, errors, and measurement data), to correctly select the section
        # of the dataframe on which to save this iteration data (the original shape of the dataframes is preserved).
        # Done this way, as the population_size may not be exactly the size of one row (even though with the default values it is).
        start_index = (
            raw_start_index
            + current_well_plate * self.blank_row_space * self.wellplate_shape[1]
        )
        end_index = start_index + self.population_size

        # store the liquid-volume data into the dataframe for this iteration
        self.liquid_volume_df.values.reshape(self.liquid_volume_df.size)[
            start_index * self.num_liquids : end_index * self.num_liquids
        ] = liquid_volumes.flatten()
        self.liquid_volume_df.to_csv(f"{self.exp_data_dir}/liquid_volumes.csv")

        # store the error data for this iteration
        self.error_df.values.reshape(self.error_df.size)[start_index:end_index] = errors
        self.error_df.to_csv(f"{self.exp_data_dir}/errors.csv")

        # only store the measurement data if it hasn't already been manually inputted into a csv.
        if self.measurement_function != "manual":
            self.measurements_df.values.reshape(self.measurements_df.size)[
                start_index
                * self.num_measured_parameters : end_index
                * self.num_measured_parameters
            ] = measurements.flatten()
            self.measurements_df.to_csv(f"{self.exp_data_dir}/measurements.csv")

        # store all the data for one iteration together (each row has the data for one well)
        iteration_idx = np.full((self.population_size, 1), self.iteration_count + 1)
        all_data = np.concatenate(
            [iteration_idx, liquid_volumes, measurements, errors[:, np.newaxis]], axis=1
        )
        start = self.iteration_count * self.population_size
        end = start + self.population_size
        self.all_data_df.iloc[start:end, :] = all_data
        self.all_data_df.to_csv(f"{self.exp_data_dir}/all_data.csv")

    def user_input(self):
        """
        Allows the user to manually input their measurement data into a csv.
        """

        total_wells = self.wellplate_shape[0] * self.wellplate_shape[1]
        raw_start_index = self.iteration_count * self.population_size
        current_well_plate = raw_start_index // total_wells

        # get start- and end-indices to index the correct section of a flattened measurements dataframe (the original shape of which is preserved).
        # Done this way, as the population_size may not be exactly the size of one row (even though with the default values it is).
        start_index = (
            raw_start_index
            + current_well_plate * self.blank_row_space * self.wellplate_shape[1]
        )
        end_index = start_index + self.population_size

        input(
            "Open 'measurements.csv', input the measurements into the corresponding row, and press any key to continue: "
        )
        measurements_df = pd.read_csv(
            f"{self.exp_data_dir}/measurements.csv", skiprows=[0], index_col=0
        )

        measurements = measurements_df.values.reshape(self.measurements_df.size)[
            start_index
            * self.num_measured_parameters : end_index
            * self.num_measured_parameters
        ]
        measurements = measurements.reshape(
            self.population_size, self.num_measured_parameters
        )
        return measurements

    def check_convergence(self, measurements):
        # close_mask is a boolean array that indicates which of the measurements fall within the
        # specified relative tolerance when compared to the target measurement.
        close_mask = np.isclose(
            measurements, self.target_measurement, rtol=self.relative_tolerance
        )  # (12, 3) in the rgb default case

        # for example, if we're measuring RGB values, we want to know whether ALL three fall within the tolerance.
        # without this, close_mask would be a boolean array for each of the rgb channels separately. In other words, we always want to make sure that each well
        # only has one boolean "closeness" value.
        close_mask = np.all(close_mask, axis=-1)

        # If any measurements fall within the specified tolerance, stop the optimisation loop
        if np.sum(close_mask) > 0:

            print(
                f"\nStopping the optimization - measurements have been found that are close to the target (within {self.relative_tolerance*100}%): "
            )

            well_row_positions = np.where(close_mask)[0]

            # print info for each close match
            for well_pos in well_row_positions:

                actual = measurements[well_pos]

                # the additional 1e-8 is in case the target_measurement is 0 - to avoid a zero division error
                percent_diff = (
                    abs(
                        (actual - self.target_measurement)
                        / (self.target_measurement + 1e-8)
                    )
                    * 100
                )
                percent_diff = np.round(percent_diff, 2)
                print(
                    f" - measurement = {actual}, percent differences of each value to the target values= {percent_diff}%"
                )

            sys.exit("Target measurement tolerance has been met — exiting the program.")

    def optimise(self, search_space, optimiser, num_iterations=8):
        if optimiser == "PSO":
            optimisers.particle_swarm(self, search_space, num_iterations)
        elif optimiser == "GP":
            optimisers.guassian_process(self, search_space, num_iterations)
        elif optimiser == "RF":
            optimisers.random_forest(self, search_space, num_iterations)
