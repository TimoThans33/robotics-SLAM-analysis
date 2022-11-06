#!/usr/bin/env python3
from pathlib import Path
import pandas as pd

class LogFile:
    @staticmethod
    def open(input_file: Path, file_type):
        input_file = Path(input_file)

        if not input_file.is_file():
            return None
        
        data_frame = pd.read_csv(input_file)
        if len(file_type) > len(data_frame.columns) \
                or not all(h.value in data_frame.columns for h in file_type):
            return None
        return data_frame