import numpy as np
import random 

def mutate_coefficients_normally_addition(selection_polynomials, mutation_rate = 0.05, **kwargs):
    mutated_polynomials = []
    for p in selection_polynomials:
        coefficients = p.coef
        mutated_coefficients = [coef+np.random.normal(0,1)*mutation_rate for coef in coefficients]
        mutated_polynomials.append(np.polynomial.polynomial.Polynomial(mutated_coefficients))
    return mutated_polynomials

def mutate_cooling(selection_polynomials, mutation_rate = 0.05, **kwargs):
    generation = kwargs.get("generation")
    cooldown = kwargs.get("cooldown")
    period = generation // cooldown
    grade = len(selection_polynomials[0].coef)
    if period >= grade:
        # print("Period of mutation is bigger than grade, no coefficients will be changed anymore. Consider increasing cooldown or decreasing number of generations.")
        pass
    mutated_polynomials = []
    for p in selection_polynomials:
        mutated_coefficients = []
        change_until = len(p.coef)-period
        for coef in p.coef[:change_until]:
            mutated_coefficients.append(coef+np.random.normal(0,1)*mutation_rate)
        for coef in p.coef[change_until:]:
            mutated_coefficients.append(coef)
        mutated_polynomials.append(np.polynomial.polynomial.Polynomial(mutated_coefficients))
    return mutated_polynomials

if __name__ == "__main__":
    grade = 5
    mylist = [np.polynomial.polynomial.Polynomial([random.random() for n in range(grade)]) for x in range(1)]
    mp = mutate_coefficients_normally_addition(mylist)
    mpc = mutate_cooling(mylist, generation =  29, cooldown = 6)
    print(mylist[0].coef)
    print(mpc[0].coef)