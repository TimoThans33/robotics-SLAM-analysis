#!/usr/bin/env python3
import matplotlib.pyplot as plt
from os.path import join

from arams.file_specifications import FMC

def save_or_show(output_folder, file_name):
    if output_folder:
        plt.savefig(join(output_folder, file_name))
        plt.close()
    else:
        plt.show()

def add_map_coordinates(arams, color=(.5, .5, .7)):
    if FMC not in arams:
        return
    
    df = arams[FMC]
    plt.scatter(df[FMC.SIG_POS_X.value], df[FMC.SIG_POS_Y.value], color=color, s=1/100)
