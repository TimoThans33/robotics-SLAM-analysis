#!/usr/bin/env python3
import os
from pathlib import Path
from typing import List

from arams.log_file import LogFile
import arams.file_specifications as file_specs

class Arams:
    # A file is identified in the folder when they start with the following strings
    _FILE_NAMES = {
        "floor_map_coordinates": file_specs.FMC,
        "logRuntimeTrackingFast": file_specs.LRT,
        "logDriftCorrections": file_specs.LDC
    }

    def __init__(self, input_paths: List[Path]):
        self._data = dict()
        if not isinstance(input_paths, list):
            input_paths = [input_paths]

        for input_path in input_paths:
            if Path(input_path).is_file():
                self._read_file(input_path)
            else:
                self._read_folder(input_path)

    def __contains__(self, file_type):
        return file_type in self._data

    def __getitem__(self, file_type):
        assert file_type in self, "Requested file type not found in inputs."
        return self._data[file_type]

    def __setitem__(self, file_type, new_data):
        self._data[file_type] = new_data
                
    def _read_folder(self, input_folder: Path):
        for root, _, files in os.walk(input_folder):
            for name in files:
                print("found: %s\n", name)
                self._read_file(Path(root) / name)
    
    def _read_file(self, input_file: Path):
        file_type = Arams._find_file_type(input_file)
        if file_type:
            data = LogFile.open(input_file, file_type)
            if data is not None:
                return self._update_data({file_type: data})

    @staticmethod
    def _find_file_type(file_name: Path):
        file_name_stem = Path(file_name).stem
        for name, file_type in Arams._FILE_NAMES.items():
            if file_name_stem.startswith(name):
                return file_type
        return None

    def _update_data(self, new_data):
        #assert not any(k in self._data for k in new_data.keys()), "Two files of the same type detected."
        self._data.update(new_data)
    