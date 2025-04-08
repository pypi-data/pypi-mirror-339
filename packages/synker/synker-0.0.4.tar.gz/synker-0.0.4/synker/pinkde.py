import numpy as np
import pandas as pd
from .kde import kde
from .scott import Scott
from .silverman import Silverman


def Pinkde(X, Y, hx, hy, bandwidth_method, grid_x, grid_y, res, min_val, max_val):
    
    if bandwidth_method is not None:
        if bandwidth_method.lower() == "scott":
            hx = Scott(X)
            hy = Scott(Y)
        elif bandwidth_method.lower() == "silverman":
            hx = Silverman(X)
            hy = Silverman(Y)
        else:
            raise ValueError("Invalid bandwidth_method. Choose 'Scott' or 'Silverman'.")
    else:
        if hx is None or hy is None:
            raise ValueError("Provide hx and hy or set bandwidth_method.")
    
    
    if grid_x is None:
        grid_x = np.linspace(min(X), max(X), res)
    if grid_y is None:
        grid_y = np.linspace(min(Y), max(Y), res)

    pkde = kde(X, Y, X, Y, hx, hy)
    
    df = pd.DataFrame({'X': X, 'Y': Y, 'pkde': np.diag(pkde), 'index': np.arange(len(X))})
    sorted_df = df.sort_values(by='pkde').reset_index(drop=True)
    sorted_df['normalized_pkde'] = (sorted_df['pkde'] - sorted_df['pkde'].min()) / (sorted_df['pkde'].max() - sorted_df['pkde'].min())

    def query_data(min_val, max_val):
        filtered_df = sorted_df[(sorted_df['normalized_pkde'] >= min_val) & (sorted_df['normalized_pkde'] <= max_val)]
        return filtered_df[['X', 'Y', 'index']]

    result = query_data(min_val, max_val)
    return result