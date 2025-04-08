"""Constants used in JWST Rogue Path Tool

Authors
-------
    - Mario Gennaro
    - Mees Fix

Use
---
    Constants in this module can be imported as follows:

    >>> from jwst_rogue_path_tool.constants import (
            CATALOG_BANDPASS,
            NIRCAM_ZEROPOINTS,
            SUSCEPTIBILITY_REGION_FULL,
            SUSCEPTIBILITY_REGION_SMALL,
            ZEROPOINT,
        )
"""

import numpy as np
import os

PROJECT_DIRNAME = os.path.dirname(__file__)

SUSCEPTIBILITY_REGION_FULL = {
    "A": np.array(
        [
            [
                2.64057,
                2.31386,
                0.47891,
                0.22949,
                -0.04765,
                -0.97993,
                -0.54959,
                0.39577,
                0.39577,
                1.08903,
                1.56903,
                2.62672,
                2.64057,
            ],
            [
                10.33689,
                10.62035,
                10.64102,
                10.36454,
                10.65485,
                10.63687,
                9.89380,
                9.47981,
                9.96365,
                9.71216,
                9.31586,
                9.93600,
                10.33689,
            ],
        ]
    ),
    "B": np.array(
        [
            [
                0.52048,
                0.03549,
                -0.28321,
                -0.49107,
                -2.80515,
                -2.83287,
                -1.58575,
                -0.51878,
                -0.51878,
                -0.40792,
                0.11863,
                0.70062,
                0.52048,
            ],
            [
                10.32307,
                10.32307,
                10.01894,
                10.33689,
                10.33689,
                9.67334,
                9.07891,
                9.63187,
                8.99597,
                8.96832,
                9.21715,
                9.70099,
                10.32307,
            ],
        ]
    ),
}

SUSCEPTIBILITY_REGION_SMALL = {
    "A": np.array(
        [
            [
                2.28483,
                0.69605,
                0.43254,
                0.57463,
                0.89239,
                1.02414,
                1.70874,
                2.28483,
                2.28483,
            ],
            [
                10.48440,
                10.48183,
                10.25245,
                10.12101,
                10.07204,
                9.95349,
                10.03854,
                10.04369,
                10.48440,
            ],
        ]
    ),
    "B": np.array(
        [
            [
                -0.96179,
                -1.10382,
                -2.41445,
                -2.54651,
                -2.54153,
                -2.28987,
                -1.69435,
                -1.46262,
                -1.11130,
                -0.95681,
                -0.59551,
                -0.58306,
                -0.96179,
            ],
            [
                10.03871,
                10.15554,
                10.15554,
                10.04368,
                9.90945,
                9.82741,
                9.76030,
                9.64347,
                9.62855,
                9.77273,
                9.88459,
                10.07848,
                10.03871,
            ],
        ]
    ),
}


NIRCAM_ZEROPOINTS = {
    "zeropoints_A": {
        "CLEAR+F070W": 7.0,
        "CLEAR+F090W": 8.0,
        "CLEAR+F182M": 9.7436,
        "CLEAR+F187N": 7.2,
        "CLEAR+F140M": 9.0,
        "F162M+F150W2": 7.5,
        "CLEAR+F212N": 8.1523,
        "CLEAR+F210M": 9.5981,
        "F164N+F150W2": 5.5,
        "CLEAR+F115W": 9.3934,
        "CLEAR+F150W": 10.2889,
        "CLEAR+F150W2": 10.88 - 0.37 - 0.1 - 0.0058,
        "CLEAR+F200W": 10.8321,
    },
    "zeropoints_B": {
        "CLEAR+F070W": 8,
        "CLEAR+F090W": 10.8491,
        "CLEAR+F182M": 10.9,
        "CLEAR+F187N": 8.3,
        "CLEAR+F140M": 9.5,
        "F162M+F150W2": 8.5,
        "CLEAR+F212N": 8.2,
        "CLEAR+F210M": 10.7,
        "F164N+F150W2": 6.5,
        "CLEAR+F115W": 9.8801,
        "CLEAR+F150W": 11.8580,
        "CLEAR+F150W2": 12.5890,
        "CLEAR+F200W": 12.0125,
    },
    "match2MASS": {
        "CLEAR+F070W": "j_m",
        "CLEAR+F090W": "j_m",
        "CLEAR+F182M": "h_m",
        "CLEAR+F187N": "h_m",
        "CLEAR+F115W": "h_m",
        "CLEAR+F140M": "h_m",
        "F162M+F150W2": "h_m",
        "CLEAR+F150W": "h_m",
        "CLEAR+F150W2": "h_m",
        "F164N+F150W2": "h_m",
        "CLEAR+F200W": "k_m",
        "CLEAR+F212N": "k_m",
        "CLEAR+F210M": "k_m",
    },
    "matchSIMBAD": {
        "CLEAR+F070W": "I",
        "CLEAR+F090W": "J",
        "CLEAR+F182M": "H",
        "CLEAR+F187N": "H",
        "CLEAR+F140M": "H",
        "F162M+F150W2": "H",
        "CLEAR+F115W": "H",
        "CLEAR+F150W": "H",
        "CLEAR+F150W2": "H",
        "F164N+F150W2": "H",
        "CLEAR+F200W": "K",
        "CLEAR+F212N": "K",
        "CLEAR+F210M": "K",
    },
}

CATALOG_BANDPASS = {"2MASS": ["j_m", "h_m", "k_m"], "SIMBAD": ["J", "H", "K"]}

ZEROPOINT = 17.0
