import copy
import random
import numpy as np

import config as cfg

from playfield import Playfield
import tetris_sim as sim

class Genome:
    def __init__(self):
        self.genes = np.array(random.sample(range(-100, 100), cfg.NUM_WEIGHTS)) / 100
        self.playgrid = Playfield()
        self.score = 0
        self.piece_count = 0

    def run(self):
        self.score, self.piece_count = sim.run_simulation(self.playgrid, self.genes)

    def uniform_crossover(self, parent1, parent2):
        for i in range(len(self.genes)):
            if(random.random() < 0.5):
                self.genes[i] = parent1.genes[i]
            else:
                self.genes[i] = parent2.genes[i]

    def scaled_crossover(self, parent1, parent2):
        total_score = parent1.score + parent2.score
        p1_odds = parent1.score / total_score
        for i in range(len(self.genes)):
            if(random.random() < p1_odds):
                self.genes[i] = parent1.genes[i]
            else:
                self.genes[i] = parent2.genes[i]

    def mutate(self):
        for gene in self.genes:
            if(random.random() < cfg.MUTATION_RATE):
                gene += random.uniform(-1 * cfg.MUTATION_RATIO, cfg.MUTATION_RATIO)

    def print_self(self):
        print("GENES = ", self.genes)
        print("SCORE = ", self.score)
        print("PIECES = ", self.piece_count)
