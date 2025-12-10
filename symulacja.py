import numpy as np
import random
from dataclasses import dataclass

# =========================
# Reprezentacja osobnika
# =========================

@dataclass
class Individual:
    x: int
    y: int
    genotype: np.ndarray  # wektor cech genetycznych


# =========================
# Inicjalizacja środowiska
# =========================

def init_environment(height: int, width: int):
    """Tworzy heterogeniczne środowisko oraz bariery."""
    # Przykładowo: wartość środowiskowa jako liczba całkowita 0..2
    env = np.random.randint(0, 3, size=(height, width))

    # Bariery: np. pionowy „mur” pośrodku siatki
    barrier = np.zeros((height, width), dtype=bool)
    mid = width // 2
    barrier[:, mid] = True  # kolumna bariery

    return env, barrier


# =========================
# Inicjalizacja populacji
# =========================

def init_population(num_individuals: int, height: int, width: int, genome_length: int):
    """Losowo rozmieszcza osobniki i nadaje im losowe genotypy."""
    population = []
    for _ in range(num_individuals):
        x = random.randrange(width)
        y = random.randrange(height)
        genotype = np.random.randint(0, 3, size=genome_length)
        population.append(Individual(x=x, y=y, genotype=genotype))
    return population


# =========================
# Funkcje modelu
# =========================

def get_neighbors(x, y, width, height):
    """Sąsiedztwo von Neumanna (góra/dół/lewo/prawo)."""
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < width - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < height - 1:
        neighbors.append((x, y + 1))
    return neighbors


def fitness(ind: Individual, env_value: int):
    """
    Prosty przykład funkcji dopasowania:
    zakładamy, że suma genotypu ma być zbliżona do wartości środowiska * 2.
    """
    target = env_value * 2
    diff = abs(ind.genotype.sum() - target)
    # im mniejsza różnica, tym większe dopasowanie (1 / (1 + diff))
    return 1.0 / (1.0 + diff)


def mutate(genotype: np.ndarray, p_mut: float):
    """Mutacje genotypu: losowa zmiana wybranych genów."""
    new_genotype = genotype.copy()
    for i in range(len(new_genotype)):
        if random.random() < p_mut:
            # losowa nowa wartość genu z zakresu 0..2
            new_genotype[i] = random.randint(0, 2)
    return new_genotype


# =========================
# Jeden krok symulacji
# =========================

def simulation_step(population, env, barrier,
                    p_mig=0.2, p_base_repro=0.1, p_mut=0.01,
                    max_per_cell=20):
    height, width = env.shape

    # 1. Migracja
    for ind in population:
        if random.random() < p_mig:
            neighbors = get_neighbors(ind.x, ind.y, width, height)
            if neighbors:
                new_x, new_y = random.choice(neighbors)
                # ruch zabroniony, jeśli to bariera
                if not barrier[new_y, new_x]:
                    ind.x, ind.y = new_x, new_y

    # 2. Rozród + mutacje (tworzymy listę potomków)
    offspring = []
    for ind in population:
        env_val = env[ind.y, ind.x]
        fit = fitness(ind, env_val)
        # prawdopodobieństwo rozrodu zależy od dopasowania
        p_repro = p_base_repro * fit
        if random.random() < p_repro:
            child_genotype = mutate(ind.genotype, p_mut)
            offspring.append(Individual(x=ind.x, y=ind.y, genotype=child_genotype))

    # 3. Dodanie potomków
    population.extend(offspring)

    # 4. Regulacja liczebności w komórkach (kapacity limit)
    #    grupujemy osobniki wg komórki i przycinamy do max_per_cell
    cell_map = {}
    for ind in population:
        cell_map.setdefault((ind.x, ind.y), []).append(ind)

    new_population = []
    for cell, inds in cell_map.items():
        if len(inds) <= max_per_cell:
            new_population.extend(inds)
        else:
            # wybieramy losowo max_per_cell osobników (można też wg dopasowania)
            new_population.extend(random.sample(inds, max_per_cell))

    return new_population


# =========================
# Główna pętla symulacji
# =========================

def run_simulation(steps=100, height=50, width=50,
                   num_individuals=200, genome_length=8):
    env, barrier = init_environment(height, width)
    population = init_population(num_individuals, height, width, genome_length)

    for t in range(steps):
        population = simulation_step(population, env, barrier)
        # tutaj można dopisać logowanie statystyk, np.:
        # - liczba osobników
        # - zróżnicowanie genotypów
        # - rozkład przestrzenny
        if t % 10 == 0:
            print(f"Krok {t}, liczba osobników: {len(population)}")

    return population, env, barrier