import matplotlib.pyplot as plt
import os
import shutil
import random

def plot_generation(polynomials_with_loss, x, scatter_y, survivors_per_generation = 3, save = False, config="", n="X"):
    polynomials_with_loss.sort(key = lambda _x: _x[1])
    fig,ax = plt.subplots()
    ax.scatter(x, scatter_y)
    
    for goodpol in polynomials_with_loss[:survivors_per_generation]:
        ax.plot(x, goodpol[0](x), color = "r")

    for badpol in polynomials_with_loss[survivors_per_generation:]:
        ax.plot(x, badpol[0](x), color = "b")

    plt.title(f"Generation {n}")
    if save:
        try:
            os.mkdir(f"./plots/{config}")
        except:
            pass
        plt.savefig(f"./plots/{config}/generation_{n}")
        plt.close()
    else:
        plt.show()
    random.shuffle(polynomials_with_loss)
    


