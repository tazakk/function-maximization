#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 12:41:30 2020

@author: Zachary Dehaan
"""

import numpy as np
import random

# This method returns the z value where z = sin(pi*10*x+10/(1+y^2))+ln(x^2+y^2)
def max_function(x, y):
    return np.float(np.sin((np.pi*10*x+10/(1+y**2)))+np.log(x**2+y**2))

# This method generates the initial population of (x,y) values. The range of x
# is any real number between 3 and 10 (inclusive). The range of y is any real
# number between 4 and 8 (inclusive). The size of the population depends on the
# parameter pop_size.
def generate_pop(pop_size):
    initial_pop = np.zeros((pop_size,2))
    for x in range(pop_size):
        initial_pop[x][0] = random.uniform(3.0,10.0)
        initial_pop[x][1] = random.uniform(4.0,8.0)
    return initial_pop

# This method calculates the fitness of a given (x,y) pair. The fitness is the
# value of f(x,y). The higher the number, the better the fitness.
def calculate_fitness(pop):
    fitness_mat = np.zeros(len(pop))
    for x in range(len(pop)):
        x_val = pop[x][0]
        y_val = pop[x][1]
        z_val = max_function(x_val,y_val)
        fitness_mat[x] = z_val
    return fitness_mat

# This method selects the parents for gene crossover by choosing the values
# with the best fitness. The number of parents to be selected is dependent on
# the parameter num_parents.
def select_parents(pop, fit_mat, num_parents):
    parents = np.zeros((num_parents, 2))
    for nums in range(num_parents):
        max_index = np.where(fit_mat == np.max(fit_mat))
        max_index = max_index[0][0]
        parents[nums] = pop[max_index]
        # prevent duplicates by setting fitness of chosen parent to small value
        fit_mat[max_index] = -999999999
    return parents

# This method implements the gene crossover between parents to produce a new
# generation of offspring. The number of offspring in the new generation is
# dependent on the parameter num_offspring. The selection process begins by
# taking one parent and grabbing its index. The parent that will produce
# offspring with the previously chosen parent is found by shifting over to the
# right. To avoid duplicates, the shift is raised by one every time the current
# index of the for-loop surpasses a multiple of the number of parents. This
# decreases redundancy and increases the variation.
def crossover(parents, num_offspring):
    offspring = np.zeros((num_offspring,2))
    shift = 1
    for num in range(num_offspring):
        x_index = num%parents.shape[0]
        if not num == 0 and num % len(parents) == 0:
            shift += 1
        y_index = (num+shift)%parents.shape[0]
        x_val = parents[x_index][0]
        y_val = parents[y_index][1]
        offspring[num] = [x_val,y_val]
    return offspring

# This method mutates the genes of the offspring by adding or subtracting a
# random float value between 0.0 and 1.0 to either the x-value or the y-value.
# The mutation alternates between choosing x-values or y-values according to
# whether the current iteration number is even or odd. The mutation only occurs
# sometimes, which is whenever a randomly generated number between 0.0 and 1.0
# is less than or equal to the probability of mutation (which is anywhere from
# 0.0 to 1.0).
def gene_mutation(offspring, probability):
    for x in range(len(offspring)):
        prob_inst = random.random()
        if prob_inst <= probability:
            random_var = random.random()
            # if we are on an even number, mutate the x-value
            if x % 2 == 0:
                val = offspring[x][0]+random_var
                if val > 10.0:
                    val = offspring[x][0]-random_var
                offspring[x][0] = val
            # for odd values, we mutate the y-value
            else:
                val = offspring[x][1]+random_var
                if val > 8.0:
                    val = offspring[x][1]-random_var
                offspring[x][1] = val
    return offspring

# This method runs the entire genetic algorithm. The number of generations in
# the algorithm depends on the parameter num_of_generations. The size of each
# population is defined by the parameter size_of_init_pop. The number of parents
# chosen in each generation is defined by the parameter num_parents. During each
# generation, the initial population is printed along with the fitness values.
# Then it prints the parents that are chosen and the resulting offspring from
# reproducing between different pairs of the parents. Then, the resulting
# offspring from the gene mutation is printed. Finally, the best result of the
# offspring is printed. After running through all generations, the best fitness
# is printed along with the associated (x,y) values. The probability of mutation
# depends on the parameter gene_mut_prob, which is a value between 0.0 and 1.0
# that signifies the probability of mutation.
def maximize_function_by_genetic_algorithm(num_of_generations, size_of_init_pop, num_parents, gene_mut_prob):
    generation = 1
    init_pop = generate_pop(size_of_init_pop)
    print "The initial population:", init_pop
    pop = init_pop
    while generation <= num_of_generations:
        print "Generation", generation, ":"
        print
        print "Fitness values:"
        fit_mat = calculate_fitness(pop)
        print fit_mat
        print
        print "Selected parents:"
        parents = select_parents(pop, fit_mat, num_parents)
        print parents
        print
        print "Gene crossover:"
        offspring = crossover(parents, size_of_init_pop)
        print offspring
        print
        print "Gene mutation:"
        offspring = gene_mutation(offspring, gene_mut_prob)
        print offspring
        print
        fitness_of_curr_pop = calculate_fitness(offspring)
        fit_max = np.max(fitness_of_curr_pop)
        if not generation == num_of_generations:
            print "Best fitness of offspring:", fit_max
        pop = offspring
        generation += 1
    fit_max_index = np.where(fitness_of_curr_pop == np.max(fitness_of_curr_pop))
    fit_max_index = fit_max_index[0][0]
    x_val = pop[fit_max_index][0]
    y_val = pop[fit_max_index][1]
    print "After", num_of_generations, "generations, the best result was:", fit_max
    print "This was achieved with x =", x_val, "and y =", y_val
    print "The probability of gene mutation was", gene_mut_prob
    
maximize_function_by_genetic_algorithm(10, 50, 20, 0.08)