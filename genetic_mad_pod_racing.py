import random
import sys
import string

alphabet = string.ascii_letters + " !'."

def get_letter():
    return random.choice(alphabet)

def mutation(chrom):
    index = random.randint(0, len(chrom) - 1)
    return chrom[:index] + get_letter() + chrom[index + 1:]


def crossover(parent1, parent2):
    child = ""
    for i in range(len(parent1)):
        if random.choice([True, False]):
            child += parent1[i]
        else:
            child += parent2[i]
    return child


def is_answer(chrom):
    return chrom == get_answer()

def evaluate_chromosome(chrom, game_state):
    # Simulez le comportement du vaisseau avec le chromosome donné et renvoyez un score basé sur ses performances
    # Par exemple, vous pouvez utiliser la distance parcourue, le nombre de checkpoints atteints, etc.
    score = 0
    # ...logique pour évaluer le chromosome...
    return score

def get_score(chrom):
    # Utilisez la fonction d'évaluation pour obtenir le score du chromosome
    game_state = {}  # Remplacez par l'état initial du jeu
    return evaluate_chromosome(chrom, game_state)


def selection(chromosomes_list):
    GRADED_RETAIN_PERCENT = 0.3
    NONGRADED_RETAIN_PERCENT = 0.2
    GRADED_RETAIN = int(len(chromosomes_list) * GRADED_RETAIN_PERCENT)
    NONGRADED_RETAIN = int(len(chromosomes_list) * NONGRADED_RETAIN_PERCENT)
    chromosomes_list.sort(key=lambda x: get_score(x), reverse=True)
    return chromosomes_list[:GRADED_RETAIN] + random.sample(
        chromosomes_list[GRADED_RETAIN:], NONGRADED_RETAIN
    )



def get_mean_score(population):
    return sum([get_score(chrom) for chrom in population]) / len(population)


def create_chromosome(size):
    return "".join([get_letter() for _ in range(size)])


def create_population(pop_size, chrom_size):
    population = [create_chromosome(chrom_size) for _ in range(pop_size)]
    return population


def generation(population):
    select = selection(population)
    children = []
    while len(children) < len(population) - len(select):
        parent1 = random.choice(select)
        parent2 = random.choice(select)
        child = crossover(parent1, parent2)
        child = mutation(child)
        children.append(child)
    return select + children


def algorithm():
    chrom_size = 10  # Taille du chromosome, ajustez selon vos besoins
    population_size = 100
    population = create_population(population_size, chrom_size)
    print(population, file=sys.stderr)
    best_chromosome = None
    best_score = -float('inf')
    generation_count = 0
    while generation_count < 1000:  # Limitez le nombre de générations pour éviter les boucles infinies
        population = generation(population)
        generation_count += 1
        print(f"Generation {generation_count}: {population}", file=sys.stderr)
        mean_score = get_mean_score(population)
        print(f"Mean score: {mean_score}", file=sys.stderr)
        for chrom in population:
            score = get_score(chrom)
            if score > best_score:
                best_score = score
                best_chromosome = chrom
        print(f"Best score: {best_score}", file=sys.stderr)
    print(f"Best chromosome found: {best_chromosome}")

def get_answer():
    return "Hello World!"


if __name__ == "__main__":
    algorithm()
