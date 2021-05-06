import numpy as np
import random 
import matplotlib.pyplot as plt
import numpy
import mutation_functions
from numpy.core.arrayprint import ComplexFloatingFormat
from selection_functions import elitist_selection
from plotting import plot_generation
import os


def simulate_polynomial(grade, coefficient_min, coefficient_max):
    coefficients = np.random.uniform(coefficient_min, coefficient_max, [grade])
    return np.polynomial.polynomial.Polynomial(coefficients)

def generate_scatter(polynom, x, scatter_multiplier, d = "default"):
    polynomial_grade = len(polynom.coef)
    distance = 10 ** (polynomial_grade)*scatter_multiplier
    if d == 0 :
        distance = 0
    size = len(x)
    scatter_y = polynom(x)+np.random.normal(0,1,size)*distance
    return scatter_y

def simulate_gridsearch(polynomial_grade,
                        coefficient_min,
                        coefficient_max,
                        x,
                        scatter_y,
                        num_generations_list,
                        survivors_per_generation_list, 
                        candidates_after_generation_list,  
                        selection_function_list, 
                        recombination_function_list, 
                        mutation_function_list,
                        elitist_list,
                        recombination_parents_list, 
                        first_mutation_rate_list,
                        cooldown_list,
                        save_plots,
                        generation_polynomials = None,
                        *args,
                        ):
    simulation_results = []
    num_simulations = len(num_generations_list) * len(survivors_per_generation_list) * len(candidates_after_generation_list) * len(selection_function_list) * len(recombination_function_list) * len(mutation_function_list) * len(elitist_list) * len(recombination_parents_list) * len(first_mutation_rate_list) * len(cooldown_list)
    print(f"Starting Gridsearch, there will be {num_simulations} simulations.")

    sim = 0 
    for num_generations in num_generations_list:
        for survivors_per_generation in survivors_per_generation_list:
            for candidates_after_generation in candidates_after_generation_list:
                for selection_function in selection_function_list:
                    for recombination_function in recombination_function_list:
                        for mutation_function in mutation_function_list:
                            for elitist in elitist_list:
                                for recombination_parents in recombination_parents_list:
                                    for first_mutation_rate in first_mutation_rate_list:
                                        for cooldown in cooldown_list:
                                            if (cooldown != 0 and mutation_function == mutation_functions.mutate_coefficients_normally_addition) or (cooldown == 0 and mutation_function == mutation_functions.mutate_cooling):
                                                print(f"Skipping simulation {sim}.")
                                                sim += 1 
                                                continue

                                            params = (
                                                polynomial_grade, coefficient_min,
                                                coefficient_max,
                                                x,
                                                scatter_y,
                                                num_generations,
                                                survivors_per_generation,
                                                candidates_after_generation,
                                                selection_function,
                                                recombination_function,
                                                mutation_function,
                                                elitist,
                                                recombination_parents,
                                                first_mutation_rate)
                                            config = get_config(*params, cooldown = cooldown)
                                            print(f"simulating config of simulation {sim}: " + config)
                                            sim += 1
                                            simudata, best_polynomial = polynomial_simulation(*params,config,
                                            save_plots = save_plots, 
                                            cooldown = cooldown)
                                            simulation_results.append((config, simudata, best_polynomial))
    return simulation_results
        

def loss_polynomial(p, x, values):
    return np.sum(np.square(values - p(x)))

def simulate_generation(polynomials,
                        survivors_per_generation, 
                        candidates_per_generation,  
                        selection_function, 
                        recombination_function, 
                        mutation_function = "None", 
                        elitist = 0, 
                        recombination_parents = 2, 
                        mutation_rate = 0.05,
                        *args,
                        **kwargs):
    """ 
    polynomials format: List[(np.Polynomial, fit)]
    
    selection_function can be one of: 
    selection_functions.
    [   
        deterministic_truncation,
        tournament_selection_with_replacement,
        tournament_selection_without_replacement,
        roulette_wheel_selection
    ]

    recombination_function can be one of:
    recombination_functions.
    [
        swap_random_parameters,
        mean_parent_parameters
    ]

    mutation_function can be one of:
    mutation_functions.
    [
        mutate_coefficients_normally_addition
    ]
    If left empty, no mutation will take place.

    If elitist is > 0: n elitists will be added to the output before recombining and mutating.
    """
    if elitist == 0 : 
        selected = selection_function(polynomials, survivors_per_generation)

        recombined = recombination_function(selected, candidates_per_generation, recombination_parents)

        mutated = mutation_function(recombined, mutation_rate = mutation_rate, **kwargs)

        return mutated
    else: 
        best, rest = elitist_selection(polynomials, elitist)
        mutated = [x[0] for x in best]
        selected = selection_function(rest, survivors_per_generation)
        recombined = recombination_function(selected, candidates_per_generation, recombination_parents)

        mutated += mutation_function(recombined, mutation_rate = mutation_rate , **kwargs)

        return mutated


def simulate_first_generation(num_candidates_per_generation, x, scatter_y, coefficient_min,coefficient_max,grade):
    generation_polynomials = []
    for num_gen in range(num_candidates_per_generation):
        p = np.polynomial.polynomial.Polynomial(np.random.uniform(coefficient_min,coefficient_max,[grade]))
        # fit = loss_polynomial(p, x , scatter_y)
        # generation_polynomials.append((p,fit))
        generation_polynomials.append(p)
    return generation_polynomials


def parse_config(config):
    splitted = config.split("$")
    out = {c:splitted[n+1] for n, c in list(enumerate(splitted))[::2]}
    return out


def get_config(
                polynomial_grade,
                coefficient_min,
                coefficient_max,
                x,
                scatter_y,
                num_generations,
                survivors_per_generation, 
                candidates_after_generation,  
                selection_function, 
                recombination_function, 
                mutation_function,
                elitist, 
                recombination_parents, 
                first_mutation_rate, 
                **kwargs):
    config_string = f"pg${polynomial_grade}$cmin${coefficient_min}$cmax${coefficient_max}$gen${num_generations}$surv${survivors_per_generation}$cand${candidates_after_generation}$selection${selection_function.__name__}$recombination${recombination_function.__name__}$mutation${mutation_function.__name__}$elitist${elitist}$numparents${recombination_parents}$mutrate${first_mutation_rate}"
    if kwargs.get("cooldown") != 0:
        config_string = config_string + "$cooldown$" + str(kwargs.get("cooldown"))
    else:
        config_string = config_string + "$cooldown$" + str(0)
    return config_string

def polynomial_simulation(
                        polynomial_grade,
                        coefficient_min,
                        coefficient_max,
                        x,
                        scatter_y,
                        num_generations,
                        survivors_per_generation, 
                        candidates_after_generation,  
                        selection_function, 
                        recombination_function, 
                        mutation_function,
                        elitist,
                        recombination_parents, 
                        first_mutation_rate,
                        config,
                        save_plots = True,
                        generation_polynomials = None,
                        *args,
                        **kwargs):
    try:
        _ = kwargs["cooldown"]
    except:
        kwargs["cooldown"] = 1

    losses = []
    

    if generation_polynomials == None:
        generation_polynomials = simulate_first_generation(candidates_after_generation,x,scatter_y, coefficient_min,coefficient_max,polynomial_grade)


    if save_plots:
        plt.ioff()

    for num_generation in range(num_generations):
        kwargs["generation"] = num_generation
        generation_polynomials_with_loss = [(p,loss_polynomial(p, x , scatter_y))  for p in generation_polynomials]
        losses.append(sum([l[1] for l in generation_polynomials_with_loss]))
        if save_plots:
            plot_generation(generation_polynomials_with_loss, x, scatter_y, survivors_per_generation= survivors_per_generation, save = save_plots, config=config, n=num_generation)
        generation_polynomials = simulate_generation(
                        generation_polynomials_with_loss,
                        survivors_per_generation, 
                        candidates_after_generation,  
                        selection_function, 
                        recombination_function, 
                        mutation_function, 
                        elitist, 
                        recombination_parents, 
                        first_mutation_rate,
                        **kwargs)
        if num_generation % 20 == 0:
            print(f"Done with generation {num_generation}")
            pass
    print("Simulation complete.")
    # plt.clf()
    # plt.plot(losses[1:])
    # plt.savefig(f"./plots/{config}/a_total_loss")
    last_generation_polynomials_with_loss = [(p,loss_polynomial(p, x , scatter_y))  for p in generation_polynomials]
    last_generation_polynomials_with_loss.sort(key = lambda _x: _x[1]) 
    best_polynomial = last_generation_polynomials_with_loss[0][0]
    return (losses,best_polynomial)
    

if __name__ == "__main__":
    grade = 5
    mylist = [(np.polynomial.polynomial.Polynomial([random.random() for n in range(grade)]),x) for x in range(10)]
    from selection_functions import deterministic_truncation
    from recombination_functions import swap_random_parameters
    from mutation_functions import mutate_coefficients_normally_addition

    m = simulate_generation(mylist, 2, 1, deterministic_truncation, swap_random_parameters, mutate_coefficients_normally_addition,1)


