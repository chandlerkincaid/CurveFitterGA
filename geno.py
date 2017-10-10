import random

import numpy as np
import functions as f


def evolve(time, xdata, arity, min_start, max_start, pop, gen, stop_num, mutation_rate,
           mutation_amount, mutation_decay, death_rate, eliteism, verbose, cur_seq):
    func = f.multi_exp
    elites = int(eliteism * pop)
    change = int(death_rate * pop)
    mutants = int(mutation_rate * pop)
    fit_offset = 10000

    class Organism:
        def __init__(self, params, fit):
            self.p = params
            self.f = fit

    def fitness(organism, f_func, f_xdata, f_time):
        y_prediction = [f_func(t, organism) for t in f_time]
        absolute_error = np.absolute(np.subtract(y_prediction, f_xdata))
        return fit_offset - np.nanmean(absolute_error)

    def crossover(parent_a, parent_b):
        both = zip(parent_a.p, parent_b.p)
        return [random.choice(x) for x in both]

    def mutate(organism, amount, chance):
        new_genes = []
        for gene in organism:
            if chance < random.random():
                new_genes.append(gene * random.uniform(-(1 + amount), (1 + amount)))
            else:
                new_genes.append(gene)
        return np.clip(new_genes, min_start, max_start)

    initial_population = [[random.uniform(min_start, max_start) for x in range(arity)] for y in range(pop)]
    population = [Organism(x, fitness(x, func, xdata, time)) for x in initial_population]
    goat = Organism(random.choice(population).p, -fit_offset)

    improving = True
    non_improving_counter = 0
    for current_gen in range(gen):
        if improving:
            fit_sum = sum([x.f for x in population])  # get total sum of fitness for use in roulette wheel
            # Roulette wheel fitness, we iterate over the population removing unlucky/unfit organisms
            most_fit = Organism([], -fit_offset)
            for x in population:
                if x.f > most_fit.f:
                    most_fit = x
            unlucky = 0
            while unlucky < change:
                endangered = random.choice(population)
                if endangered.f / fit_sum < random.random():
                    population.remove(endangered)
                    unlucky += 1
            # Create new organisms, also roulette wheel selection(for half)
            while len(population) < pop:
                potential = random.choice(population)
                if potential.f / fit_sum > random.random():
                    child = crossover(random.choice(population), potential)
                    population.append(Organism(child, fitness(child, func, xdata, time)))
            for mut in range(mutants):
                selected = random.choice(population)
                population.remove(selected)  # delete selected from population
                new_mutant = mutate(selected.p, mutation_amount, 0.4)
                population.append(Organism(new_mutant, fitness(new_mutant, func, xdata, time)))
            new_elite = 0
            while new_elite < elites:
                population.remove(random.choice(population))
                population.append(random.choice([goat, most_fit]))
                new_elite += 1
            mutation_amount *= mutation_decay  # decay mutation amount each generation
            # fitness statistics
            average_fit = np.mean([x.f for x in population])
            most_fit2 = Organism([],-fit_offset)
            for x in population:
                if x.f > most_fit2.f:
                    most_fit2 = x
            if most_fit2.f > goat.f:
                goat = most_fit2
                non_improving_counter = 0
                mutation_amount = 0.3
            else:
                non_improving_counter += 1
            print("Data: " + str(cur_seq + 1) + " Gen : " + str(current_gen) + " Non-Improve: "
                  + str(non_improving_counter))
            # print("GenBest: " + "%.4f" % (most_fit.f - fit_offset))
            print("GlobalBest: " + "%.8f" % (goat.f - fit_offset))
            # print(goat.p)
            if verbose:
                print("Average: " + str(average_fit - fit_offset))
                print("GenBest: " + str(most_fit.p))
                print("GlobalBest: " + str(goat.p))
                # print_formula(goat.p)
                print("\n")
            if non_improving_counter >= stop_num:
                improving = False
    print(goat.p)
    return goat.p



