import numpy as np
import random
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.spatial.distance import pdist, squareform
import warnings
warnings.filterwarnings('ignore')

# =========================
# PARAMETRY SYMULACJI
# =========================

class SimulationConfig:
    """Konfiguracja parametrów symulacji"""
    def __init__(self):
        self.height = 50
        self.width = 50
        self.num_individuals = 300
        self.genome_length = 8
        self.steps = 200
        
        # Parametry genetyczne
        self.p_mutation = 0.02  # prawdopodobieństwo mutacji
        self.p_migration = 0.15  # prawdopodobieństwo migracji
        self.p_base_repro = 0.12  # bazowe prawdopodobieństwo rozrodu
        self.max_per_cell = 25  # max osobników w komórce
        
        # Typy barier
        self.barrier_type = "vertical"  # "vertical", "horizontal", "none"


# =========================
# Reprezentacja osobnika
# =========================

@dataclass
class Individual:
    x: int
    y: int
    genotype: np.ndarray  # wektor cech genetycznych
    birth_time: int = 0


# =========================
# Inicjalizacja środowiska
# =========================

def init_environment(height: int, width: int, barrier_type: str = "vertical"):
    """Tworzy heterogeniczne środowisko oraz bariery."""
    # Wartość środowiskowa jako liczba całkowita 0..2
    env = np.random.randint(0, 3, size=(height, width))
    
    # Tworzenie barier
    barrier = np.zeros((height, width), dtype=bool)
    
    if barrier_type == "vertical":
        # Pionowa bariera w połowie szerokości
        mid = width // 2
        barrier[:, mid] = True
    elif barrier_type == "horizontal":
        # Pozioma bariera w połowie wysokości
        mid = height // 2
        barrier[mid, :] = True
    elif barrier_type == "none":
        # Brak barier
        pass
    
    return env, barrier


# =========================
# Inicjalizacja populacji
# =========================

def init_population(num_individuals: int, height: int, width: int, 
                   genome_length: int, initial_time: int = 0):
    """Losowo rozmieszcza osobniki i nadaje im losowe genotypy."""
    population = []
    for _ in range(num_individuals):
        x = random.randrange(width)
        y = random.randrange(height)
        genotype = np.random.randint(0, 3, size=genome_length)
        population.append(Individual(x=x, y=y, genotype=genotype, birth_time=initial_time))
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
    Funkcja dopasowania:
    suma genotypu powinna być zbliżona do wartości środowiska * 2.
    Zwraca wartość z przedziału [0, 1].
    """
    target = env_value * 2
    diff = abs(ind.genotype.sum() - target)
    return 1.0 / (1.0 + diff)


def mutate(genotype: np.ndarray, p_mut: float):
    """Mutacje genotypu: losowa zmiana wybranych genów."""
    new_genotype = genotype.copy()
    for i in range(len(new_genotype)):
        if random.random() < p_mut:
            new_genotype[i] = random.randint(0, 2)
    return new_genotype


def can_move(x1, y1, x2, y2, barrier):
    """Sprawdza czy ruch jest możliwy (nie przecina bariery)."""
    return not barrier[y2, x2]


# =========================
# Jeden krok symulacji
# =========================

def simulation_step(population: List[Individual], env: np.ndarray, 
                   barrier: np.ndarray, current_time: int,
                   config: SimulationConfig):
    """Jeden krok symulacji obejmujący migrację, rozród i selekcję."""
    height, width = env.shape
    
    # 1. Migracja
    for ind in population:
        if random.random() < config.p_migration:
            neighbors = get_neighbors(ind.x, ind.y, width, height)
            if neighbors:
                new_x, new_y = random.choice(neighbors)
                if can_move(ind.x, ind.y, new_x, new_y, barrier):
                    ind.x, ind.y = new_x, new_y
    
    # 2. Rozród + mutacje
    offspring = []
    for ind in population:
        env_val = env[ind.y, ind.x]
        fit = fitness(ind, env_val)
        p_repro = config.p_base_repro * fit
        
        if random.random() < p_repro:
            child_genotype = mutate(ind.genotype, config.p_mutation)
            offspring.append(Individual(x=ind.x, y=ind.y, 
                                       genotype=child_genotype, 
                                       birth_time=current_time))
    
    # 3. Dodanie potomków
    population.extend(offspring)
    
    # 4. Regulacja liczebności w komórkach
    cell_map = {}
    for ind in population:
        cell_map.setdefault((ind.x, ind.y), []).append(ind)
    
    new_population = []
    for cell, inds in cell_map.items():
        if len(inds) <= config.max_per_cell:
            new_population.extend(inds)
        else:
            # Losowy wybór (można też zastosować selekcję wg dopasowania)
            new_population.extend(random.sample(inds, config.max_per_cell))
    
    return new_population


# =========================
# Zbieranie danych
# =========================

@dataclass
class SimulationStats:
    """Statystyki z każdego kroku symulacji"""
    time: int
    population_size: int
    mean_fitness: float
    genetic_diversity: float
    left_pop_size: int = 0  # liczba osobników po lewej stronie bariery
    right_pop_size: int = 0  # liczba osobników po prawej stronie bariery


class DataCollector:
    """Zbiera dane statystyczne z symulacji"""
    def __init__(self, barrier: np.ndarray):
        self.barrier = barrier
        self.stats: List[SimulationStats] = []
        self.genotype_history: List[List[np.ndarray]] = []
    
    def collect(self, population: List[Individual], env: np.ndarray, 
               current_time: int, config: SimulationConfig):
        """Zbiera statystyki z danego kroku"""
        if not population:
            return
        
        # Liczba osobników
        pop_size = len(population)
        
        # Średnia wartość dopasowania
        fitnesses = [fitness(ind, env[ind.y, ind.x]) for ind in population]
        mean_fitness = np.mean(fitnesses) if fitnesses else 0
        
        # Różnorodność genetyczna (jako średnia odległość Hamminga)
        if len(population) > 1:
            genotypes = np.array([ind.genotype for ind in population])
            # Odległość Hamminga (liczba różnych genów)
            distances = pdist(genotypes, metric='hamming')
            genetic_diversity = np.mean(distances) if len(distances) > 0 else 0
        else:
            genetic_diversity = 0
        
        # Liczba osobników po każdej stronie bariery
        barrier_x = np.where(self.barrier[0])[0]
        if len(barrier_x) > 0:
            barrier_pos = barrier_x[0]
            left_pop = sum(1 for ind in population if ind.x < barrier_pos)
            right_pop = pop_size - left_pop
        else:
            left_pop = pop_size
            right_pop = 0
        
        # Zapisanie statystyk
        stats = SimulationStats(
            time=current_time,
            population_size=pop_size,
            mean_fitness=mean_fitness,
            genetic_diversity=genetic_diversity,
            left_pop_size=left_pop,
            right_pop_size=right_pop
        )
        self.stats.append(stats)
        
        # Zapisanie genotypów do historii
        genotypes = [ind.genotype.copy() for ind in population]
        self.genotype_history.append(genotypes)


# =========================
# Analiza genetyki populacji
# =========================

def calculate_population_genetic_distance(population_left: List[Individual], 
                                         population_right: List[Individual]) -> float:
    """Oblicza średnią odległość genetyczną między dwiema populacjami."""
    if not population_left or not population_right:
        return 0
    
    genotypes_left = np.array([ind.genotype for ind in population_left])
    genotypes_right = np.array([ind.genotype for ind in population_right])
    
    # Średnia różnica w genotypach
    mean_left = np.mean(genotypes_left, axis=0)
    mean_right = np.mean(genotypes_right, axis=0)
    
    genetic_distance = np.mean(np.abs(mean_left - mean_right))
    return genetic_distance


def detect_species_clusters(population: List[Individual], 
                           threshold: float = 0.3) -> Tuple[List[List[Individual]], float]:
    """
    Detektuje potencjalne skupiska (incipient species) na podstawie podobieństwa genetycznego.
    Zwraca listę klastrów oraz średnią różnorodność wewnątrz i między klastrami.
    """
    if len(population) < 2:
        return [population], 0
    
    genotypes = np.array([ind.genotype for ind in population])
    distances = squareform(pdist(genotypes, metric='hamming'))
    
    # Prosty algorytm klastrowania: osobniki o podobieństwie > (1-threshold) 
    # są w tym samym klastrze
    clusters = []
    assigned = set()
    
    for i, ind in enumerate(population):
        if i in assigned:
            continue
        
        cluster = [ind]
        assigned.add(i)
        
        for j in range(i + 1, len(population)):
            if j in assigned:
                continue
            if distances[i, j] < threshold:
                cluster.append(population[j])
                assigned.add(j)
        
        clusters.append(cluster)
    
    return clusters, np.mean(distances)


# =========================
# Wizualizacja
# =========================

def plot_simulation_snapshot(population: List[Individual], env: np.ndarray,
                            barrier: np.ndarray, title: str = "Snapshot"):
    """Rysuje snapshota stanu symulacji"""
    height, width = env.shape
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Lewy panel: Środowisko i rozmieszczenie populacji
    ax = axes[0]
    im = ax.imshow(env, cmap='YlGn', origin='lower', alpha=0.3)
    
    # Narysuj bariery
    for x in range(width):
        for y in range(height):
            if barrier[y, x]:
                ax.add_patch(Rectangle((x - 0.5, y - 0.5), 1, 1, 
                                       fill=True, color='red', alpha=0.5))
    
    # Narysuj osobniki (kolor zależy od genotypu)
    if population:
        xs = [ind.x for ind in population]
        ys = [ind.y for ind in population]
        colors = [np.mean(ind.genotype) for ind in population]
        scatter = ax.scatter(xs, ys, c=colors, cmap='RdYlBu', s=30, alpha=0.6, edgecolors='black', linewidth=0.5)
        plt.colorbar(scatter, ax=ax, label='Średni genotyp')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'{title}\nRozmieszczenie populacji (liczba: {len(population)})')
    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    
    # Prawy panel: Histogram genotypów
    ax = axes[1]
    if population:
        all_alleles = np.concatenate([ind.genotype for ind in population])
        ax.hist(all_alleles, bins=3, color='skyblue', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Wartość allelu')
        ax.set_ylabel('Liczba alleli')
        ax.set_title('Rozkład alleli w populacji')
    
    plt.tight_layout()
    return fig


def plot_simulation_results(collector: DataCollector, barrier: np.ndarray, 
                           config: SimulationConfig):
    """Rysuje wykresy wyników symulacji"""
    if not collector.stats:
        print("Brak danych do wykreślenia!")
        return
    
    times = [s.time for s in collector.stats]
    pop_sizes = [s.population_size for s in collector.stats]
    fitnesses = [s.mean_fitness for s in collector.stats]
    diversities = [s.genetic_diversity for s in collector.stats]
    left_pops = [s.left_pop_size for s in collector.stats]
    right_pops = [s.right_pop_size for s in collector.stats]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Liczba osobników w populacji
    ax = axes[0, 0]
    ax.plot(times, pop_sizes, 'b-', linewidth=2, label='Razem')
    if config.barrier_type != "none":
        ax.plot(times, left_pops, 'r--', linewidth=1.5, label='Lewa strona')
        ax.plot(times, right_pops, 'g--', linewidth=1.5, label='Prawa strona')
    ax.set_xlabel('Czas (kroki)')
    ax.set_ylabel('Liczba osobników')
    ax.set_title('Dynamika liczebności populacji')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Średnie dopasowanie
    ax = axes[0, 1]
    ax.plot(times, fitnesses, 'g-', linewidth=2)
    ax.set_xlabel('Czas (kroki)')
    ax.set_ylabel('Średnie dopasowanie')
    ax.set_title('Ewolucja średniego dopasowania')
    ax.grid(True, alpha=0.3)
    
    # Różnorodność genetyczna
    ax = axes[1, 0]
    ax.plot(times, diversities, 'purple', linewidth=2)
    ax.set_xlabel('Czas (kroki)')
    ax.set_ylabel('Różnorodność genetyczna')
    ax.set_title('Zmienność genetyczna w populacji')
    ax.grid(True, alpha=0.3)
    
    # Liczba osobników po każdej stronie bariery (jeśli istnieje)
    ax = axes[1, 1]
    if config.barrier_type != "none" and (any(left_pops) or any(right_pops)):
        ax.stackplot(times, left_pops, right_pops, 
                    labels=['Lewa strona', 'Prawa strona'],
                    colors=['red', 'green'], alpha=0.6)
        ax.set_xlabel('Czas (kroki)')
        ax.set_ylabel('Liczba osobników')
        ax.set_title('Rozkład populacji w zależności od bariery')
        ax.legend(loc='upper left')
    else:
        ax.text(0.5, 0.5, 'Brak bariery', ha='center', va='center', 
               transform=ax.transAxes, fontsize=12)
        ax.set_title('Rozkład populacji')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


# =========================
# Główna pętla symulacji
# =========================

def run_simulation(config: SimulationConfig = None, verbose: bool = True):
    """Uruchamia pełną symulację z zbieraniem danych i analizą"""
    if config is None:
        config = SimulationConfig()
    
    # Inicjalizacja
    env, barrier = init_environment(config.height, config.width, config.barrier_type)
    population = init_population(config.num_individuals, config.height, 
                                config.width, config.genome_length)
    collector = DataCollector(barrier)
    
    if verbose:
        print(f"=== SYMULACJA FORMOWANIA SIĘ GATUNKÓW ===")
        print(f"Parametry:")
        print(f"  - Wymiary siatki: {config.width}x{config.height}")
        print(f"  - Typ bariery: {config.barrier_type}")
        print(f"  - Liczba osobników: {config.num_individuals}")
        print(f"  - Liczba kroków: {config.steps}")
        print(f"  - Długość genotypu: {config.genome_length}")
        print()
    
    # Główna pętla
    for t in range(config.steps):
        population = simulation_step(population, env, barrier, t, config)
        collector.collect(population, env, t, config)
        
        if verbose and t % 20 == 0:
            print(f"Krok {t:3d}: {len(population):3d} osobników, "
                  f"dopasowanie: {collector.stats[-1].mean_fitness:.3f}, "
                  f"różnorodność: {collector.stats[-1].genetic_diversity:.3f}")
    
    if verbose:
        print(f"\nSymulacja zakończona!")
        print(f"Końcowa liczba osobników: {len(population)}")
    
    return population, env, barrier, collector


# =========================
# Uruchomienie
# =========================

if __name__ == "__main__":
    # Test 1: Symulacja z pionową barierą
    print("\n" + "="*60)
    print("TEST 1: SYMULACJA Z PIONOWĄ BARIERĄ")
    print("="*60 + "\n")
    
    config = SimulationConfig()
    config.barrier_type = "vertical"
    config.steps = 200
    config.num_individuals = 300
    
    population, env, barrier, collector = run_simulation(config, verbose=True)
    
    # Snapshoty z różnych etapów
    fig1 = plot_simulation_snapshot(population, env, barrier, 
                                    f"Stan końcowy (krok {config.steps})")
    plt.savefig('/home/andrzej/Studia/Modelowanie i symulacja systemów/projekt/snapshot_final.png', 
                dpi=100, bbox_inches='tight')
    print("Zapisano snapshot końcowy: snapshot_final.png")
    
    # Wykresy wyników
    fig2 = plot_simulation_results(collector, barrier, config)
    plt.savefig('/home/andrzej/Studia/Modelowanie i symulacja systemów/projekt/results_barrier.png', 
                dpi=100, bbox_inches='tight')
    print("Zapisano wykresy wyników: results_barrier.png")
    
    # Analiza genetyczna
    barrier_x = np.where(barrier[0])[0]
    if len(barrier_x) > 0:
        barrier_pos = barrier_x[0]
        left_pop = [ind for ind in population if ind.x < barrier_pos]
        right_pop = [ind for ind in population if ind.x >= barrier_pos]
        
        print(f"\n=== ANALIZA GENETYCZNA ===")
        print(f"Liczba osobników po lewej stronie: {len(left_pop)}")
        print(f"Liczba osobników po prawej stronie: {len(right_pop)}")
        
        if left_pop and right_pop:
            gen_dist = calculate_population_genetic_distance(left_pop, right_pop)
            print(f"Średnia odległość genetyczna między populacjami: {gen_dist:.4f}")
            print("(wyższa wartość = większa divergencja genetyczna = specjacja)")
    
    # Test 2: Symulacja bez bariery (dla porównania)
    print("\n" + "="*60)
    print("TEST 2: SYMULACJA BEZ BARIERY (KONTROLA)")
    print("="*60 + "\n")
    
    config2 = SimulationConfig()
    config2.barrier_type = "none"
    config2.steps = 200
    config2.num_individuals = 300
    
    population2, env2, barrier2, collector2 = run_simulation(config2, verbose=True)
    
    fig3 = plot_simulation_results(collector2, barrier2, config2)
    plt.savefig('/home/andrzej/Studia/Modelowanie i symulacja systemów/projekt/results_no_barrier.png', 
                dpi=100, bbox_inches='tight')
    print("Zapisano wykresy: results_no_barrier.png")
    
    # Porównanie
    print(f"\n=== PORÓWNANIE ===")
    print(f"Z barierą - końcowa różnorodność: {collector.stats[-1].genetic_diversity:.4f}")
    print(f"Bez bariery - końcowa różnorodność: {collector2.stats[-1].genetic_diversity:.4f}")
    print(f"(Bariera powinna zmniejszać różnorodność, ale zwiększać divergencję między populacjami)")
    
    plt.show()


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
# Analiza genetyki populacji (DODANE)
# =========================

def analyze_genetic_divergence(populations):
    """
    Analizuje divergencję genetyczną między populacjami.
    
    Args:
        populations: lista populacji (każda to lista osobników)
    
    Returns:
        float: średnia divergencja genetyczna (0-1)
    """
    if len(populations) < 2:
        return 0.0
    
    divergences = []
    
    for i in range(len(populations)):
        for j in range(i + 1, len(populations)):
            pop_i = populations[i]
            pop_j = populations[j]
            
            if len(pop_i) == 0 or len(pop_j) == 0:
                continue
            
            # Obliczenie średniej różnicy alleli między populacjami
            genotypes_i = np.array([ind.genotype for ind in pop_i])
            genotypes_j = np.array([ind.genotype for ind in pop_j])
            
            avg_genotype_i = np.mean(genotypes_i, axis=0)
            avg_genotype_j = np.mean(genotypes_j, axis=0)
            
            # Euklidesowa odległość między średnimi genotypami
            distance = np.linalg.norm(avg_genotype_i - avg_genotype_j)
            divergences.append(distance)
    
    if divergences:
        return np.mean(divergences)
    return 0.0


def visualize_comparison(populations, environment, barriers, collection, title, filename):
    """
    Wizualizuje stan końcowy populacji.
    
    Args:
        populations: lista populacji
        environment: mapa środowiska
        barriers: mapa barier
        collection: dane zbierane podczas symulacji
        title: tytuł wykresu
        filename: nazwa pliku do zapisania
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(title, fontsize=14, fontweight='bold')
    
    # 1. Rozkład populacji na mapie
    ax = axes[0, 0]
    grid_size = environment.shape[0]
    
    # Pokaż środowisko (note: imshow shows (y,x) with y increasing downward by default)
    im = ax.imshow(environment, cmap='RdYlBu_r', alpha=0.6, origin='lower')
    plt.colorbar(im, ax=ax, label='Warunki środowiska')
    
    # Pokaż bariery
    if barriers is not None:
        for y in range(grid_size):
            for x in range(grid_size):
                if barriers[y, x] > 0:
                    ax.add_patch(Rectangle((x - 0.5, y - 0.5), 1, 1, 
                                          fill=True, color='black', alpha=0.5))
    
    # Pokaż populacje (różne kolory)
    colors = plt.cm.Set3(np.linspace(0, 1, len(populations)))
    for pop_idx, population in enumerate(populations):
        if len(population) > 0:
            positions = np.array([[ind.x, ind.y] for ind in population])
            ax.scatter(positions[:, 0], positions[:, 1], c=[colors[pop_idx]], 
                      s=50, alpha=0.7, label=f'Pop {pop_idx + 1}')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Rozkład przestrzenny populacji')
    ax.legend(loc='upper right', fontsize=8)
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(-0.5, grid_size - 0.5)
    
    # 2. Dynamika liczby osobników
    ax = axes[0, 1]
    if 'total_population' in collection:
        ax.plot(collection['total_population'], linewidth=2, color='#2ecc71')
        ax.fill_between(range(len(collection['total_population'])), 
                        collection['total_population'], alpha=0.3, color='#2ecc71')
        ax.set_xlabel('Generacja')
        ax.set_ylabel('Liczba osobników')
        ax.set_title('Dynamika populacji')
        ax.grid(True, alpha=0.3)
    
    # 3. Różnorodność genetyczna
    ax = axes[1, 0]
    if 'genetic_diversity' in collection:
        ax.plot(collection['genetic_diversity'], linewidth=2, color='#3498db')
        ax.fill_between(range(len(collection['genetic_diversity'])), 
                        collection['genetic_diversity'], alpha=0.3, color='#3498db')
        ax.set_xlabel('Generacja')
        ax.set_ylabel('Różnorodność genetyczna')
        ax.set_title('Ewolucja różnorodności')
        ax.grid(True, alpha=0.3)
    
    # 4. Statystyki
    ax = axes[1, 1]
    ax.axis('off')
    
    stats_text = f"""
    STATYSTYKI KOŃCOWE
    {'='*40}
    
    Liczba populacji: {len(populations)}
    
    Rozmiary populacji:
    """
    
    for i, pop in enumerate(populations):
        stats_text += f"\n  Populacja {i + 1}: {len(pop)} osobników"
    
    total_pop = sum(len(p) for p in populations)
    stats_text += f"\n\n  RAZEM: {total_pop} osobników"
    
    # Divergencja genetyczna
    div = analyze_genetic_divergence(populations)
    stats_text += f"\n\nDywergencja genetyczna: {div:.4f}"
    
    if len(populations) > 1:
        stats_text += "\n(Wyższa wartość → więcej specjacji)"
    
    ax.text(0.1, 0.5, stats_text, fontsize=10, family='monospace',
            verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  Wizualizacja zapisana: {filename}")


# =========================
# Główna pętla symulacji
# =========================

def run_simulation(config=None):
    """
    Uruchamia główną symulację.
    
    Args:
        config: słownik z parametrami lub None dla domyślnych
    
    Returns:
        tuple: (populations, environment, barriers, collection)
    """
    # Parametry domyślne
    if config is None:
        config = {}
    
    grid_size = config.get('grid_size', 10)
    initial_pop_size = config.get('initial_pop_size', 100)
    generations = config.get('generations', 100)
    mutation_rate = config.get('mutation_rate', 0.05)
    barrier_type = config.get('barrier_type', 'none')
    barrier_position = config.get('barrier_position', 5)
    
    # Inicjalizacja
    height = width = grid_size
    environment = init_environment(height, width, barrier_type)
    barriers = environment[1] if isinstance(environment, tuple) else None
    environment = environment[0] if isinstance(environment, tuple) else environment
    
    population = init_population(initial_pop_size, height, width, genome_length=8)
    
    # Zbiór danych
    collection = {
        'total_population': [],
        'genetic_diversity': [],
        'fitness': [],
        'num_populations': []
    }
    
    # Symulacja
    for gen in range(generations):
        population = simulation_step(population, environment, barriers, 
                                    p_mig=0.15, p_base_repro=0.12, p_mut=mutation_rate,
                                    max_per_cell=25)
        
        # Zbieranie danych
        total_pop = len(population)
        collection['total_population'].append(total_pop)
        
        # Różnorodność genetyczna
        if len(population) > 0:
            genotypes = np.array([ind.genotype for ind in population])
            if len(genotypes) > 1:
                distances = pdist(genotypes, metric='hamming')
                diversity = np.mean(distances) if len(distances) > 0 else 0
            else:
                diversity = 0
            collection['genetic_diversity'].append(diversity)
        else:
            collection['genetic_diversity'].append(0)
    
    # Grupowanie populacji po stronach bariery (jeśli istnieje)
    populations = []
    if barrier_type == 'vertical' and barriers is not None:
        barrier_x = np.where(barriers[0])[0]
        if len(barrier_x) > 0:
            barrier_pos = barrier_x[0]
            left_pop = [ind for ind in population if ind.x < barrier_pos]
            right_pop = [ind for ind in population if ind.x >= barrier_pos]
            if left_pop:
                populations.append(left_pop)
            if right_pop:
                populations.append(right_pop)
        else:
            populations = [population]
    else:
        populations = [population]
    
    return populations, environment, barriers, collection