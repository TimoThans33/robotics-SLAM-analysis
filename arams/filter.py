#!/usr/bin/env python3
import numpy as np
from pandas import DataFrame

from arams import Arams
import arams.file_specifications as file_spec
from utils.argument_parser import parse_arguments

class LastPowerCycleFilter:
    @staticmethod
    def filter_all(arams: Arams):
        for file_type in [file_spec.LRT, file_spec.LDC]:
            if file_type in arams:
                LastPowerCycleFilter.filter(arams, file_type)
    
    @staticmethod
    def filter(arams: Arams, file_type):
        if file_type not in arams:
            raise Exception("Filter data of supplied type not possible as data is not available.")

        if not any(e for e in file_type if e.value.lower() == "index"):
            raise Exception("No 'index' field in supplied type.")
        index_column_name = [e for e in file_type if e.value.lower() == "index"][0].value

        data = arams[file_type]
        index_data = data[index_column_name]
        last_power_cycle_index = LastPowerCycleFilter.get_last_power_cycle_index(index_data)

        if last_power_cycle_index != 0:
            arams[file_type] = data.loc[last_power_cycle_index:]

    @staticmethod
    def get_last_power_cycle_index(data: DataFrame):
        data = np.array(data)
        data_diff = np.diff(data)
        row_indices = np.where(data_diff < 0)[0].tolist()

        # Note that the + 1 is required as the row index was determined based on the data difference list which has one
        # element less
        return row_indices[-1] + 1 if row_indices else 0


if __name__ == "__main__":  
    args = parse_arguments()
    arams = Arams(args["input"])

    LastPowerCycleFilter.filter_all(arams)