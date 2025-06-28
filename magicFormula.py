

import numpy as np
import pandas as pd

def fit_using_magic_formula():
    """
    y = D*sin(C*arctan(B*x-E*(B*x-arctan(B*x))))

    Coefficients B, C, D, and E are computed to form line of best fit for Fx, Fy, and Mz wrt to Fz, IA, and beta
    """

