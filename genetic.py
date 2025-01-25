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

def get_score(chrom):
    key = get_answer()
    score = 0
    for i in range(len(key)):
        if key[i] == chrom[i]:
            score += 1
    return score / len(key)


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
    answer = get_answer()
    chrom_size = len(answer)
    population_size = 100
    population = create_population(population_size, chrom_size)
    print(population, file=sys.stderr)
    answers = []
    generation_count = 0
    while not answers:
        population = generation(population)
        generation_count += 1
        print(population, file=sys.stderr)
        print(get_mean_score(population), file=sys.stderr)
        print(generation_count, file=sys.stderr)
        for chrom in population:
            if is_answer(chrom):
                answers.append(chrom)
        if generation_count > 1000:
            break
    print(answers[0])

def get_answer():
    return "Hello World!"


if __name__ == "__main__":
    algorithm()
