# Polynometic - using genetic algorithms to approximate polynomials

In this project, I tried to use a genetic algorithm to approximate a polynomial of a given degree. 
The input is a cloud of measurement points, that is generated from an unknown polyinomial that is being added with normally distributed noise, 

All parameters can be set interactively with jupyter widgets. 

## Example 
Since this is a very interactive project, it's best to have a graphic example 
on how it works. Enjoy!


https://user-images.githubusercontent.com/42912323/117483111-96b60100-af65-11eb-8d41-7e90c0266a83.mp4


## Installation  
Create and activate a virtual environment to be able to install the dependencies with a fresh python copy, then install the requirements:
    
    $ python -m venv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

## Usage
Open a new jupyter notebook session:

    $ jupyter notebook

You can run the notebook cell by cell, you can chose between a range of selection functions, 
recombination functions and mutation functions. 
For the Selection functions you can chose between:
* deterministic_truncation
* tournament_selection_with_replacement
* tournament_selection_without_replacement
* roulette_wheel_selection
* elitist_selection

For the recombination functions you can chose between:
* swap_random_parameters 
* mean_parent_parameters

For the mutation functions you can chose between:
* mutate_coefficients_normally_addition
* mutate_cooling 

Beside the different functions, you can set some of the general parameters, like
how many generations there are, how many candidates will be generated for each 
generation and how many survivors we have for each generation. 

After setting all the options and determining how the polynomial that the genetic 
algorithm has to learn is supposed to look like, you can start the simulation. 
After it is done, you can see how the different generations approximated the polynomial 
and which one has been the best solution

