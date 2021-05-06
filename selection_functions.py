import random
import numpy as np

def deterministic_truncation(generation_polynomials, n):
    generation_polynomials.sort(key = lambda _x: _x[1]) 
    return [x[0] for x in generation_polynomials[:n]]

def tournament_selection_with_replacement(generation_polynomials, n):
    winners = []
    for trial in range (n):
        competitor1 = random.choice(generation_polynomials)
        competitor2 = random.choice(generation_polynomials)
        # print(f" now fighting {str(competitor1)} vs {str(competitor1)}")
        winner = competitor1 if competitor1[1] < competitor2[1] else competitor2
        # print(f"winner is {winner}")
        winners.append(winner)
    return [x[0] for x in winners]

def tournament_selection_without_replacement(generation_polynomials):
    """ Has the wrong interaface and will thus not be used for now.
    """
    random.shuffle(generation_polynomials)
    generation_polynomials = generation_polynomials[:-1] if len(generation_polynomials)%2 == 1 else generation_polynomials
    pairs = [(x, generation_polynomials[n+1]) for n,x in enumerate(generation_polynomials) if n %2 == 0]
    winners = []
    for pair in pairs:
        # print(f" now fighting {str(pair[0])} vs {str(pair[1])}")
        winner = pair[0] if pair[0][1] < pair[1][1] else pair[1]
        # print(f"winner is {winner}")
        winners.append(winner)
    return [x[0] for x in winners]

def roulette_wheel_selection(generation_polynomials, n):
    total_fitness = sum([fit[1] for fit in generation_polynomials])
    probabilities = [p[1]/total_fitness for p in generation_polynomials]
    l = list(range(len(generation_polynomials)))
    winners = np.random.choice(l, n, p=probabilities)
    return [generation_polynomials[x][0] for x in winners]

def elitist_selection(generation_polynomials, n):
    generation_polynomials.sort(key = lambda _x: _x[1]) 
    best = generation_polynomials[:n]
    rest = generation_polynomials[n:]
    return (best,rest)
    
if __name__ == "__main__":
    mylist = [(f"polynom: {x}", x) for x in range(100)]