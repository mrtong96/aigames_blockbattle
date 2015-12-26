
import random
import board
from board import matrix_to_list

def magnitude(feature_vector):
    return sum(map(lambda x: x ** 2, feature_vector.values())) ** .5

def normalize(feature_vector):
    multiplier = 1.0 / magnitude(feature_vector)
    return {k: v * multiplier for k, v in feature_vector.iteritems()}

def init_random_normal_vector(args):
    result = dict(map(lambda x: (x, random.random() * 2 - 1), args))
    return normalize(result)

def mutate(feature_vector):
    name = random.choice(feature_vector.keys())
    feature_vector[name] += .4 * (random.random() - .5)
    return normalize(feature_vector)

def combine(mem0, mem1, mut_chance=0.0):
    fitness0, weight0 = mem0
    fitness1, weight1 = mem1

    new_vector = {k: fitness0 * weight0[k] + fitness1 * weight1[k] for k in weight0.keys()}
    new_vector = normalize(new_vector)
    if random.random() < mut_chance:
        new_vector = mutate(new_vector)
    return new_vector

class GeneticAlgorithm(object):
    def __init__(self, features, pop_size, num_iterations, fitness_function):
        self.features = features
        self.pop_size = pop_size
        self.num_iterations = num_iterations
        self.fitness_function = fitness_function

        self.mut_chance = .05
        self.gen_replaced = .3
        self.population = self.initialize_population()

    def run_GA(self):
        for i in range(self.num_iterations):
            fitness_members = map(lambda x: (self.fitness_function(x), x), self.population)

            new_generation = []
            for j in range(int(self.gen_replaced * self.pop_size + .5)):
                selection = random.sample(fitness_members, 100)
                mem0 = max(selection, key=lambda x: x[0])
                selection.remove(mem0)
                mem1 = max(selection, key=lambda x: x[0])

                new_generation.append(combine(mem0, mem1, self.mut_chance))

            fitness_members.sort(key=lambda x: - x[0])
            print 'iteration: {}, fittest member: {}'.format(i, fitness_members[0])
            fitness_members = fitness_members[0: int((1 - self.gen_replaced) * self.pop_size + .5)]
            self.population = map(lambda x: x[1], fitness_members) + new_generation 

        fitness_members = map(lambda x: (self.fitness_function(x), x), self.population)
        fittest_member = max(fitness_members, key=lambda x: x[0])[1]
        return fittest_member

    def initialize_population(self):
        pop = []
        for i in range(self.pop_size):
            pop.append(init_random_normal_vector(self.features))
        return pop

# trying to get the GA to stack everything in a width-3 wide column on the left.
class StackerBoard(board.Board):
    
    def get_feature_vector(self):
        feature_vector = {}
        row_data = map(lambda row: map(lambda x: 1 if x > 1 else 0, row), self.data)
        col_data = zip(*row_data)

        def highest(col):
            ht = self.height
            for el in col:
                if el:
                    break
                ht -= 1
            return ht

        highest_cols = map(lambda col: highest(col), col_data[:-3])
        feature_vector['sum_tower'] = sum(highest_cols)

        highest_cols = map(lambda col: highest(col), col_data[-3:])
        feature_vector['sum_valley'] = sum(highest_cols)

        tower_rows = map(lambda row: reduce(lambda x, y: x and y, row[:-3]), row_data)
        feature_vector['tower_lines'] = sum(tower_rows)

        height_diffs = []
        for i in range(len(highest_cols) - 1):
            height_diffs.append(abs(highest_cols[i] - highest_cols[i + 1]))
        feature_vector['sum_tower_height_diffs'] = sum(height_diffs)

        spaces = map(lambda row: map(lambda x: 1 if not x else 0, row), row_data)
        spaces = matrix_to_list(spaces)

        not_holes = set(filter(lambda x: x[1] == 0, spaces))

        fringe = not_holes.copy()
        while len(fringe):
            x, y = fringe.pop()
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for neighbor in neighbors:
                if neighbor in spaces and neighbor not in not_holes:
                    not_holes.add(neighbor)
                    fringe.add(neighbor)

        holes = set(spaces) - not_holes
        feature_vector['hole_tower'] = len(filter(lambda x: x[0] < self.width-3, holes))

        return feature_vector
    
def test_GA0():
    features = ['a','b','c']
    import math
    fitness_function = lambda x: math.sin(x['a']) - math.cos(x['b']) + math.tan(x['c'])
    GA = GeneticAlgorithm(features, 1000, 50, fitness_function)
    print GA.run_GA()

#test_GA0()
