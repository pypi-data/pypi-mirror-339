"""
The function minimization by checking all solutions in a grid
-------------------------------------------------------------

..
    :copyright:
        Jan Wiszniowski (jwisz@igf.edu.pl)
    :license:
        GNU Lesser General Public License, Version 3
        (https://www.gnu.org/copyleft/lesser.html)
    :version 0.0.1:
        2024-11-07

"""

import numpy as np
import matplotlib.pyplot as plt


class RetClass:
    def __init__(self, x, error):
        self.success = True
        self.x = x
        self.error = error


def grid_search(function, x, args=None):
    """
    It minimizes the function by checking all solutions in a grid.

    :param function: The minimized function
    :type function: func
    :param x: Initial values (not used, only for compatibility)
    :type x: list
    :param args: The minimized function arguments. It must be the configuration dictionary.
    :type args: list
    :return: The minimization result
    :rtype: RetClass
    """
    if isinstance(args, tuple):
        args = args[0]
    if args['optimization']['method'] != 'grid_search':
        raise Exception('It must be grid search optimization')
    input_range = args['optimization']['mw']
    mw = np.arange(input_range[0], input_range[1], input_range[2])
    input_range = args['optimization']['log_f0']
    f_0 = np.arange(input_range[0], input_range[1], input_range[2])
    min_err = 1e20
    min_mw = -1
    min_f_0 = -1
    for idx_f_0 in range(len(f_0)):
        for idx_mw in range(len(mw)):
            err = function([mw[idx_mw], f_0[idx_f_0]])
            if err < min_err:
                min_err = err
                min_mw = idx_mw
                min_f_0 = idx_f_0
    # error = function([mw[min_mw], f_0[min_f_0]], args)
    error = function([mw[min_mw], f_0[min_f_0]])
    return RetClass([mw[min_mw], f_0[min_f_0]], error)

# def grid_search(function, x, source_parameters=None):
#     if isinstance(source_parameters, tuple):
#         source_parameters = source_parameters[0]
#     if source_parameters.configuration['optimization']['method'] != 'grid_search':
#         raise Exception('It must be grid search optimization')
#     input_range = source_parameters.configuration['optimization']['mw']
#     mw = np.arange(input_range[0], input_range[1], input_range[2])
#     input_range = source_parameters.configuration['optimization']['log_f0']
#     f_0 = np.arange(input_range[0], input_range[1], input_range[2])
#     min_err = 1e20
#     min_mw = -1
#     min_f_0 = -1
#     for idx_f_0 in range(len(f_0)):
#         for idx_mw in range(len(mw)):
#             err = function([mw[idx_mw], f_0[idx_f_0]], source_parameters)
#             if err < min_err:
#                 min_err = err
#                 min_mw = idx_mw
#                 min_f_0 = idx_f_0
#     error = function([mw[min_mw], f_0[min_f_0]], source_parameters)
#     return RetClass([mw[min_mw], f_0[min_f_0]], error)
