import numpy as np
import random 


def swap_random_parameters(selection_polynomials, num_candidates_per_generation, numparents = 2):
    """ Swaps random coefficients of N-selected parents.
    """
    candidates = []
    while len(candidates)<num_candidates_per_generation:
        parents = random.sample(selection_polynomials,numparents) 
        coefficients = []
        for c in range(len(parents[0].coef)):
            whichparent = np.random.randint(numparents)
            coefficients.append(parents[whichparent].coef[c])
        candidates.append(np.polynomial.polynomial.Polynomial(coefficients))
    return candidates

def mean_parent_parameters(selection_polynomials, num_candidates_per_generation, numparents = 2):
    """ Computes mean of N-selected parents.
    """
    candidates = []
    while len(candidates)<num_candidates_per_generation:
        parents = random.sample(selection_polynomials,numparents) 
        parents_coefficients = [p.coef for p in parents]
        # print(parents_coefficients)
        mean_coefficients = np.mean(parents_coefficients,axis=0)
        candidates.append(np.polynomial.polynomial.Polynomial(mean_coefficients))
    return candidates



if __name__ == "__main__":
    grade = 5
    mylist = [np.polynomial.polynomial.Polynomial([random.random() for n in range(grade)]) for x in range(10)]
    # c = swap_random_parameters(mylist,1,3)
    m = mean_parent_parameters(mylist,1,3)
    