import copy
import random
import numpy as np

import config as cfg

from genome import Genome
import tetris_sim as sim

population = [Genome() for count in range(cfg.POPULATION_SIZE)]
for indiv in population:
    indiv.run()

population.sort(key=lambda x: x.score, reverse=True)

generation = 1
print("TOTAL GENERATIONS: ", cfg.NUM_GENERATIONS)

while(generation <= cfg.NUM_GENERATIONS):
    print("CURRENT GENERATION: ", generation)
    offspring = []
    parent_pool = population[: cfg.POPULATION_SIZE //  2]
    while(len(offspring) < cfg.POPULATION_SIZE * 9 // 10):
        parent1, parent2 = random.sample(parent_pool, 2)
        child1 = Genome()
        child1.uniform_crossover(parent1, parent2)
        child1.mutate()
        child1.run()
        child2 = Genome()
        child2.scaled_crossover(parent1, parent2)
        child2.mutate()
        child2.run()
        offspring.append(child1)
        offspring.append(child2)

    population = population[: cfg.POPULATION_SIZE // 10] + offspring
    population.sort(key=lambda x: x.score, reverse=True)
    print("POPULATION_SIZE: ", len(population))
    print("BEST GENOME FOR THIS GEN ")
    population[0].print_self()
    generation += 1

print("POPULATION LENGTH: ", len(population))
population[0].print_self()
population[0].playgrid.print_self()
population[1].print_self()
population[1].playgrid.print_self()
population[2].print_self()
population[2].playgrid.print_self()
# population[20].print_self()
# # population[20].playgrid.print_self()
# population[34].print_self()
# # population[34].playgrid.print_self()
# population[50].print_self()
# # population[50].playgrid.print_self()
# population[97].print_self()
# population[97].playgrid.print_self()
# population[98].print_self()
# population[98].playgrid.print_self()
# population[99].print_self()
# population[99].playgrid.print_self()
