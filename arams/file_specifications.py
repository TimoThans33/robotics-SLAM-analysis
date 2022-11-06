#!/usr/bin/env python3
from enum import Enum

# Floor map coordinates .csv file column headers used
class FMC(Enum):
    IDX_IN_MAP = "idxInMap"
    CLUSTER_ID = "clusterID"
    SIG_STATUS = "sigStatus"
    SIG_POS_X = "sigPosX"
    SIG_POS_Y = "sigPosY"


# Log runtime tracking .csv file column headers used
class LRT(Enum):
    INDEX = "index"
    TIME = "time[ms]"
    INPUT_POSE_X = "inputPoseX[m]"
    INPUT_POSE_Y = "inputPoseY[m]"
    INPUT_POSE_TH = "inputPoseTh[rad]"
    OUTPUT_POSE_X = "outputPoseX[m]"
    OUTPUT_POSE_Y = "outputPoseY[m]"
    OUTPUT_POSE_TH = "outputPoseTh[rad]"

# Log drift corrections .csv file column headers used
class LDC(Enum):
    INDEX = "index"
    TIME = "time[ms]"
    NEW_XPOS = "New_xpos[m]"
    NEW_YPOS = "New_ypos[m]"
    NEW_THETA = "New_theta[rad]"
    ERROR_X = "Error_x[m]"
    ERROR_Y = "Error_y[m]"
    ERROR_THETA = "Error_theta[rad]"
    CUMU_DIST = "Cumulative distance[m]"
    CLUSTER_ID = "Cluster ID"
    SIGNATURE_ID = "Signature ID"