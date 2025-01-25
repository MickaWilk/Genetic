import sys
import math
import random

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Fitness function
def fitness(individual, x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_angle):
    target_x, target_y, thrust = individual
    dist = distance(target_x, target_y, next_checkpoint_x, next_checkpoint_y)
    angle_penalty = abs(next_checkpoint_angle) / 180.0
    return -1 * (dist + angle_penalty * 100)

# Generate initial population
def generate_population(pop_size, x, y, next_checkpoint_x, next_checkpoint_y):
    population = []
    for _ in range(pop_size):
        target_x = random.randint(next_checkpoint_x - 500, next_checkpoint_x + 500)
        target_y = random.randint(next_checkpoint_y - 500, next_checkpoint_y + 500)
        thrust = random.choice([0, 50, 100, "BOOST"])
        population.append([target_x, target_y, thrust])
    return population

# Crossover
def crossover(parent1, parent2):
    child = [
        (parent1[0] + parent2[0]) // 2,
        (parent1[1] + parent2[1]) // 2,
        random.choice([parent1[2], parent2[2]])
    ]
    return child

# Mutation
def mutate(individual):
    if random.random() < 0.1:
        individual[0] += random.randint(-100, 100)
        individual[1] += random.randint(-100, 100)
    if random.random() < 0.1:
        individual[2] = random.choice([0, 50, 100, "BOOST"])
    return individual

# Genetic algorithm
def genetic_algorithm(x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_angle, generations=10, pop_size=20):
    population = generate_population(pop_size, x, y, next_checkpoint_x, next_checkpoint_y)
    for _ in range(generations):
        # Evaluate fitness
        population = sorted(population, key=lambda ind: fitness(ind, x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_angle), reverse=True)
        # Select the best individuals
        best_individuals = population[:pop_size // 2]
        # Create new generation
        new_population = best_individuals[:]
        while len(new_population) < pop_size:
            p1, p2 = random.sample(best_individuals, 2)
            child = crossover(p1, p2)
            child = mutate(child)
            new_population.append(child)
        population = new_population
    return population[0]

# Game loop
while True:
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]
    
    # Run genetic algorithm
    best_individual = genetic_algorithm(x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_angle)
    
    # Output the best command
    target_x, target_y, thrust = best_individual
    print(f"{int(target_x)} {int(target_y)} {thrust}")
