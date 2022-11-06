#!/usr/bin/env python3
import argparse
import os.path

def validate_argument_is_dir(path):
    if not os.path.isdir(path):
        return ValueError("Supplied output folder does not exist.")
    return path

def parse_arguments(velocity=False):
    parser = argparse.ArgumentParser()

    # Default arguments
    parser.add_argument("-i", "--input", required=True, nargs="+",
                        help="Input file(s) and folder(s)")
    parser.add_argument("-o", "--output", required=False, type=validate_argument_is_dir,
                        help="Output folder in which figures are stored")
    parser.add_argument("-d", "--debug", required=False, type=bool, default=False,
                        help="Please specify if debug mode is desired")

    # Configurable arguments
    if velocity:
        parser.add_argument("-v", "--velocity", required=True, type=float,
                            help="The velocity during mapping in m/s")

    return vars(parser.parse_args())