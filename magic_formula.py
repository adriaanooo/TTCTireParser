import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def mf52(alpha, kappa, gamma, fz):
    """
    y = D*sin(C*arctan(B*x-E*(B*x-arctan(B*x))))

    Coefficients B, C, D, and E are computed to form line of best fit for Fx, Fy, and Mz wrt to Fz, IA, and beta
    """
    return D * np.sin(C * np.arctan(B * x - E * (B * x - np.arctan(B * x))))
