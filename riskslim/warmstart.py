import time
import numpy as np
from cplex import Cplex, SparsePair, infinity as CPX_INFINITY
from riskslim.solution_pool import SolutionPool
from riskslim.bound_tightening import chained_updates, chained_updates_for_lp
from riskslim.heuristics import discrete_descent, sequential_rounding
from riskslim.data import Bounds
from riskslim.defaults import DEFAULT_CPA_SETTINGS
from riskslim.utils import print_log, validate_settings


def run_standard_cpa(cpx,
                     cpx_indices,
                     compute_loss,
                     compute_loss_cut,
                     settings = DEFAULT_CPA_SETTINGS,
                     print_flag = True):

    assert isinstance(cpx, Cplex)
    assert isinstance(cpx_indices, dict)
    assert callable(compute_loss)
    assert callable(compute_loss_cut)
    assert isinstance(settings, dict)

    settings = validate_settings(settings, defaults = DEFAULT_CPA_SETTINGS)

    rho_idx = cpx_indices["rho"]
    loss_idx = cpx_indices["loss"]
    alpha_idx = cpx_indices["alpha"]
    cut_idx = loss_idx + rho_idx
    objval_idx = cpx_indices["objval"]
    L0_idx = cpx_indices["L0_norm"]

    P = len(cpx_indices["rho"])
    C_0_alpha = np.array(cpx_indices['C_0_alpha'])
    C_0_nnz = C_0_alpha[np.flatnonzero(C_0_alpha)]

    if isinstance(loss_idx, list) and len(loss_idx) == 1:
        loss_idx = loss_idx[0]

    if len(alpha_idx) > 0:
        get_alpha = lambda: np.array(cpx.solution.get_values(alpha_idx))
    else:
        get_alpha = lambda: np.array([])

    bounds = Bounds(
        loss_min=cpx.variables.get_lower_bounds(loss_idx),
        loss_max=cpx.variables.get_upper_bounds(loss_idx),
        objval_min=cpx.variables.get_lower_bounds(objval_idx),
        objval_max=cpx.variables.get_upper_bounds(objval_idx),
        L0_min=cpx.variables.get_lower_bounds(L0_idx),
        L0_max=cpx.variables.get_upper_bounds(L0_idx),
    )

    if settings['update_bounds'] and settings['type'] == 'cvx':
        update_bounds = lambda bounds, lb, ub: chained_updates_for_lp(bounds, C_0_nnz, ub, lb)
    elif settings['update_bounds'] and settings['type'] == 'ntree':
        update_bounds = lambda bounds, lb, ub: chained_updates(bounds, C_0_nnz, ub, lb)
    else:
        update_bounds = lambda bounds, lb, ub: bounds

    objval = 0.0
    upperbound = CPX_INFINITY
    lowerbound = 0.0
    n_iterations = 0
    n_simplex_iterations = 0
    max_runtime = float(settings['max_runtime'])
    max_cplex_time = float(settings['max_runtime_per_iteration'])
    remaining_total_time = max_runtime
    solutions = []
    objvals = []

    progress_stats = {
        'upperbounds': [],
        'lowerbounds': [],
        'simplex_iterations': [],
        'cut_times': [],
        'total_times': []
        }

    run_start_time = time.time()
    while True:

        iteration_start_time = time.time()
        cpx.parameters.timelimit.set(min(remaining_total_time, max_cplex_time))
        cpx.solve()
        solution_status = cpx.solution.status[cpx.solution.get_status()]

        # get solution
        if solution_status not in ('optimal', 'optimal_tolerance', 'MIP_optimal'):
            stop_reason = solution_status
            stop_msg = 'stopping CPA | solution is infeasible (status = %s)' % solution_status
            break

        # get solution
        rho = np.array(cpx.solution.get_values(rho_idx))
        alpha = get_alpha()
        simplex_iterations = int(cpx.solution.progress.get_num_iterations())

        # compute cut
        cut_start_time = time.time()
        loss_value, loss_slope = compute_loss_cut(rho)
        cut_lhs = [float(loss_value - loss_slope.dot(rho))]
        cut_constraint = [SparsePair(ind = cut_idx, val = [1.0] + (-loss_slope).tolist())]
        cut_time = time.time() - cut_start_time

        # compute objective bounds
        objval = float(loss_value + alpha.dot(C_0_alpha))
        upperbound = min(upperbound, objval)
        lowerbound = cpx.solution.get_objective_value()
        relative_gap = (upperbound - lowerbound)/(upperbound + np.finfo('float').eps)
        bounds = update_bounds(bounds, lb = lowerbound, ub = upperbound)

        #store solutions
        solutions.append(rho)
        objvals.append(objval)

        # update run stats
        n_iterations += 1
        n_simplex_iterations += simplex_iterations
        current_time = time.time()
        total_time = current_time - run_start_time
        iteration_time = current_time - iteration_start_time
        remaining_total_time = max(max_runtime - total_time, 0.0)

        # print progress
        if print_flag and settings['display_progress']:
            print_log("cuts = %d \t UB = %.4f \t LB = %.4f \t GAP = %.4f%%\n" % (n_iterations, upperbound, lowerbound, 100.0 * relative_gap))

        # save progress
        if settings['save_progress']:
            progress_stats['upperbounds'].append(upperbound)
            progress_stats['lowerbounds'].append(lowerbound)
            progress_stats['total_times'].append(total_time)
            progress_stats['cut_times'].append(cut_time)
            progress_stats['simplex_iterations'].append(simplex_iterations)

        # check termination conditions
        if n_iterations >= settings['max_iterations']:
            stop_reason = 'aborted:reached_max_cuts'
            stop_msg = 'reached max iterations'
            break

        if n_iterations >= settings['min_iterations_before_coefficient_gap_check']:
            prior_rho = solutions[-2]
            coef_gap = np.abs(np.max(rho - prior_rho))
            if np.all(np.round(rho) == np.round(prior_rho)) and coef_gap < settings['max_coefficient_gap']:
                stop_reason = 'aborted:coefficient_gap_within_tolerance'
                stop_msg = 'stopping CPA | coef gap is within tolerance (%1.4f < %1.4f)' % (coef_gap, settings['max_coefficient_gap'])
                break

        if relative_gap < settings['max_tolerance']:
            stop_reason = 'converged:gap_within_tolerance'
            stop_msg = 'stopping CPA | optimality gap is within tolerance (%1.1f%% < %1.1f%%)' % (100 * settings['max_tolerance'], 100 * relative_gap)
            break

        if iteration_time > settings['max_runtime_per_iteration']:
            stop_reason = 'aborted:reached_max_train_time'
            stop_msg = 'stopping CPA (reached max training time per iteration of %1.0f secs)' % settings['max_runtime_per_iteration']
            break

        if (total_time > settings['max_runtime']) or (remaining_total_time == 0.0):
            stop_reason = 'aborted:reached_max_train_time'
            stop_msg = 'stopping CPA (reached max training time of %1.0f secs)' % settings['max_runtime']
            break

        # switch bounds
        if settings['update_bounds']:
            cpx.variables.set_lower_bounds(L0_idx, bounds.L0_min
                                           )
            cpx.variables.set_upper_bounds(L0_idx, bounds.L0_max)
            cpx.variables.set_lower_bounds(loss_idx, bounds.loss_min)
            cpx.variables.set_upper_bounds(loss_idx, bounds.loss_max)
            cpx.variables.set_lower_bounds(objval_idx, bounds.objval_min)
            cpx.variables.set_upper_bounds(objval_idx, bounds.objval_max)

        # add loss cut
        cpx.linear_constraints.add(lin_expr = cut_constraint, senses = ["G"], rhs = cut_lhs)

    if print_flag:
        print_log(stop_msg)

    #collect stats
    stats = {
        'solution': rho,
        'stop_reason': stop_reason,
        'n_iterations': n_iterations,
        'n_simplex_iterations': n_simplex_iterations,
        'objval': objval,
        'upperbound': upperbound,
        'lowerbound': lowerbound,
        'cut_time': cut_time,
        'total_time': total_time,
        'cplex_time': total_time - cut_time,
        }

    stats.update(bounds.asdict())
    if settings['save_progress']:
        progress_stats['cplex_times'] = (np.array(stats['total_times']) - np.array(stats['cut_times'])).tolist()
        progress_stats['objvals'] = objvals
        progress_stats['solutions'] = solutions
        stats.update(progress_stats)

    #collect cuts
    idx = list(range(cpx_indices['n_constraints'], cpx.linear_constraints.get_num(), 1))
    cuts = {
        'coefs': cpx.linear_constraints.get_rows(idx),
        'lhs': cpx.linear_constraints.get_rhs(idx)
        }

    #create solution pool
    pool = SolutionPool(P)
    if len(objvals) > 0:
        pool.add(objvals, solutions)

    return stats, cuts, pool



def round_solution_pool(pool,
                        constraints,
                        max_runtime = float('inf'),
                        max_solutions = float('inf')):
    """

    Parameters
    ----------
    pool
    constraints
    max_runtime
    max_solutions

    Returns
    -------

    """
    # quick return
    if len(pool) == 0:
        return pool

    pool = pool.distinct().sort()
    P = pool.P
    L0_reg_ind = np.isnan(constraints['coef_set'].c0)
    L0_max = constraints['L0_max']


    total_runtime = 0.0
    total_rounded = 0
    rounded_pool = SolutionPool(P)

    for rho in pool.solutions:

        start_time = time.time()
        # sort from largest to smallest coefficients
        feature_order = np.argsort([-abs(x) for x in rho])
        rounded_solution = np.zeros(shape = (1, P))
        l0_norm_count = 0

        for k in range(P):
            j = feature_order[k]
            if not L0_reg_ind[j]:
                rounded_solution[0, j] = np.round(rho[j], 0)
            elif l0_norm_count < L0_max:
                rounded_solution[0, j] = np.round(rho[j], 0)
                l0_norm_count += L0_reg_ind[j]

        total_runtime += time.time() - start_time
        total_rounded += 1
        rounded_pool.add(objvals = np.nan, solutions = rounded_solution)

        if total_runtime > max_runtime or total_rounded >= max_solutions:
            break

    rounded_pool = rounded_pool.distinct().sort()
    return rounded_pool, total_runtime, total_rounded


def sequential_round_solution_pool(pool,
                                   Z,
                                   C_0,
                                   compute_loss_from_scores_real,
                                   get_L0_penalty,
                                   max_runtime = float('inf'),
                                   max_solutions = float('inf'),
                                   objval_cutoff = float('inf')):

    """
    runs sequential rounding for all solutions in a solution pool
    can be stopped early using max_runtime or max_solutions

    Parameters
    ----------
    pool
    Z
    C_0
    compute_loss_from_scores_real
    get_L0_penalty
    max_runtime
    max_solutions
    objval_cutoff
    L0_min
    L0_max

    Returns
    -------

    """
    # quick return
    if len(pool) == 0:
        return pool, 0.0, 0

    assert callable(get_L0_penalty)
    assert callable(compute_loss_from_scores_real)

    # if model size constraint is non-trivial, remove solutions that violate the model size constraint beforehand
    pool = pool.distinct().sort()
    rounding_handle = lambda rho: sequential_rounding(rho = rho,
                                                      Z = Z,
                                                      C_0 = C_0,
                                                      compute_loss_from_scores_real = compute_loss_from_scores_real,
                                                      get_L0_penalty = get_L0_penalty,
                                                      objval_cutoff = objval_cutoff)


    # apply sequential rounding to all solutions
    total_runtime = 0.0
    total_rounded = 0
    rounded_pool = SolutionPool(pool.P)

    for rho in pool.solutions:

        start_time = time.time()
        solution, objval, early_stop = rounding_handle(rho)
        total_runtime += time.time() - start_time
        total_rounded += 1

        if not early_stop:
            rounded_pool = rounded_pool.add(objvals = objval, solutions = solution)

        if total_runtime > max_runtime or total_rounded > max_solutions:
            break

    rounded_pool = rounded_pool.distinct().sort()
    return rounded_pool, total_runtime, total_rounded


def discrete_descent_solution_pool(pool,
                                   Z,
                                   C_0,
                                   constraints,
                                   get_L0_penalty,
                                   compute_loss_from_scores,
                                   max_runtime = float('inf'),
                                   max_solutions = float('inf')):
    """

    runs dcd polishing for all solutions in a solution pool
    can be stopped early using max_runtime or max_solutions


    Parameters
    ----------
    pool
    Z
    C_0
    constraints
    get_L0_penalty
    compute_loss_from_scores
    max_runtime
    max_solutions

    Returns
    -------

    """

    pool = pool.remove_nonintegral()
    if len(pool) == 0:
        return pool, 0.0, 0

    assert callable(get_L0_penalty)
    assert callable(compute_loss_from_scores)

    rho_ub = constraints['coef_set'].ub
    rho_lb = constraints['coef_set'].lb

    polishing_handle = lambda rho: discrete_descent(rho,
                                                    Z = Z,
                                                    C_0 = C_0,
                                                    rho_ub = rho_ub,
                                                    rho_lb = rho_lb,
                                                    get_L0_penalty = get_L0_penalty,
                                                    compute_loss_from_scores = compute_loss_from_scores)
    pool = pool.distinct().sort()

    polished_pool = SolutionPool(pool.P)
    total_runtime = 0.0
    total_polished = 0
    start_time = time.time()
    for rho in pool.solutions:
        polished_solution, _, polished_objval = polishing_handle(rho)
        total_runtime = time.time() - start_time
        total_polished += 1
        polished_pool = polished_pool.add(objvals = polished_objval, solutions = polished_solution)
        if total_runtime > max_runtime or total_polished >= max_solutions:
            break

    polished_pool = polished_pool.distinct().sort()
    return polished_pool, total_runtime, total_polished
