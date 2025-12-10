# KARTA SZYBKIEGO DOSTĘPU

## Struktura Plików

```
species-formation-simulation/
│
├─ symulacja.py                    ← Główny moduł (URUCHOM TEN)
├─ run_simulations.py              ← Wielowariantowe eksperymenty
├─ quickstart.py                   ← 4 proste przykłady
├─ config_gallery.py               ← 13 predefiniowanych scenariuszy
│
├─ README.md                       ← Dokumentacja techniczna
├─ DOKUMENTACJA_NAUKOWA.md         ← Biologia i matematyka
└─ KARTA_SZYBKIEGO_DOSTĘPU.md      ← Ten plik
```

---

## Jak Uruchomić

### OPCJA 1: Standardowa Symulacja (NAJPROSTSZA)
```bash
python3 symulacja.py
```
✓ Uruchamia 2 symulacje (z barierą + bez bariery)  
✓ Generuje wykresy PNG  
✓ Wyświetla analizę genetyczną  

### OPCJA 2: Wielowariantowe Eksperymenty
```bash
python3 run_simulations.py           # Wszystkie 3 eksperymenty
python3 run_simulations.py 1         # Tylko eksperyment 1
python3 run_simulations.py 2         # Tylko eksperyment 2
python3 run_simulations.py 3         # Tylko eksperyment 3
```

### OPCJA 3: Szybki Start (TUTORIAL)
```bash
python3 quickstart.py
```
✓ 4 praktyczne przykłady  
✓ Wyjaśnienia każdego kroku  

### OPCJA 4: Galeria Konfiguracji (BADAŃ)
```bash
python3 config_gallery.py
```
✓ 13 predefiniowanych scenariuszy  
✓ Porównania między wariantami  

---

## Zmiana Parametrów

### Metoda 1: Poprzez Kod
```python
from symulacja import SimulationConfig, run_simulation

config = SimulationConfig()

# Zmień parametry
config.barrier_type = "horizontal"    # zmień typ bariery
config.steps = 300                    # zmień liczbę kroków
config.num_individuals = 500          # zmień populację
config.p_mutation = 0.05              # zmień mutacyjność
config.p_migration = 0.10             # zmień migrację

# Uruchom
population, env, barrier, collector = run_simulation(config)
```

### Metoda 2: Poprzez Galerię Konfiguracji
```python
from config_gallery import ConfigGallery

# Pobierz gotową konfigurację
config = ConfigGallery.get('extreme')      # ekstremalna izolacja
# lub
config = ConfigGallery.get('large_pop')    # duża populacja
```

### Dostępne Parametry
```
config.height              = 50              # Wysokość siatki
config.width               = 50              # Szerokość siatki
config.num_individuals     = 300             # Liczba osobników
config.genome_length       = 8               # Długość genotypu
config.steps               = 200             # Liczba kroków

config.p_mutation          = 0.02            # Mutacje (0-1)
config.p_migration         = 0.15            # Migracja (0-1)
config.p_base_repro        = 0.12            # Rozród (0-1)
config.max_per_cell        = 25              # Max osobników/komórka

config.barrier_type        = "vertical"      # "vertical", "horizontal", "none"
```

---

## Interpretacja Wyników

### snapshot_final.png
- **Lewy panel**: Mapa populacji
  - Każdy punkt = osobnik
  - Kolor = średni genotyp (niski=czerwony, wysoki=niebieski)
  - Czerwone kwadraty = bariery
  
- **Prawy panel**: Histogram alleli
  - Pokazuje rozkład wartości genetycznych

### results_barrier.png (lub results_no_barrier.png)

**Górny lewy**: Liczba osobników
- Niebieska linia = całkowita populacja
- Jeśli jest bariera: czerwona (lewa) i zielona (prawa)
- Rosnący = populacja się rozmnażała
- Malejący = brak wystarczającego rozrodu

**Górny prawy**: Średnie dopasowanie
- Wyższa = lepsze przystosowanie
- Powinno rosnąć szybko, potem się ustabilizować
- Plateau wskazuje osiągnięcie optimum

**Dolny lewy**: Różnorodność genetyczna
- Wyższa = większa zmienność w populacji
- Zwykle maleje (fokus na allele, które działają)
- Z barierą: malejąca szybciej (izolacja)

**Dolny prawy**: Rozkład względem bariery
- Pokazuje, czy populacje rozbiegają się do różnych rozmiarów
- Wskazuje na niezależną ewolucję populacji

---

## Szybka Analiza

```python
# Wczytaj wyniki
from symulacja import SimulationConfig, run_simulation

config = SimulationConfig()
pop, env, bar, col = run_simulation(config, verbose=False)

# Wyodrębnij dane
stats = col.stats
final = stats[-1]

print(f"Końcowa populacja: {final.population_size}")
print(f"Fitness: {final.mean_fitness:.4f}")
print(f"Różnorodność: {final.genetic_diversity:.4f}")

# Poróweń początek i koniec
print(f"Zmiana populacji: {final.population_size - stats[0].population_size}")
print(f"Zmiana diversity: {final.genetic_diversity - stats[0].genetic_diversity:.4f}")
```

---

## Przewodnik Wyników

### Oczekiwane Zakresy

| Metryka | Z Barierą | Bez Bariery | Interpretacja |
|---------|-----------|-------------|---------------|
| Divergencja | 0.3-0.5 | <0.1 | Wyższy = większa specjacja |
| Final Pop | Różne | Jednolita | Bariera = niezależne sub-popy |
| Fitness | >0.6 | >0.6 | Powinno rosnąć z czasu |
| Diversity | <0.2 | >0.2 | Bariera zmniejsza wewnętrzną div. |

### Co Oznacza Specjacja?
- ✅ Divergencja genetyczna > 0.3
- ✅ Różne allele w każdej populacji
- ✅ Malejąca wewnętrzna zmienność
- ✅ Sub-populacje ewoluują niezależnie

---

## Godzina Po Godzinie

### Jeśli masz 5 minut
```bash
python3 symulacja.py
# Zobaczysz wyniki w konsoli i PNG
```

### Jeśli masz 15 minut
```bash
python3 quickstart.py
# 4 przykłady z wyjaśnieniami
```

### Jeśli masz 30 minut
```bash
python3 run_simulations.py
# 3 kompleksowe eksperymenty
# Przeczytaj DOKUMENTACJA_NAUKOWA.md
```

### Jeśli masz 1+ godzinę
```bash
# Spróbuj własnych parametrów
# Zmodyfikuj symulacja.py
# Wykreśl własne porównania
# Przeczytaj całą dokumentację
```

---

## Rozwiązywanie Problemów

### Błąd: "No module named 'numpy'"
```bash
pip install numpy matplotlib scipy
```

### Błąd: "python3: command not found"
```bash
which python  # zamiast python3
python symulacja.py
```

### Wyniki nie pokazują się
```python
# Upewnij się, że masz matplotlib
import matplotlib
matplotlib.use('Agg')  # Użyj Agg backend jeśli brak display
```

### Symulacja jest za wolna
```python
# Zmniejsz parametry:
config.steps = 50           # Zamiast 200
config.num_individuals = 100  # Zamiast 300
config.height = 25          # Zamiast 50
config.width = 25
```

---

## Gotowe Skrypty Do Kopiowania

### Test 1: Podstawowy
```python
from symulacja import SimulationConfig, run_simulation, plot_simulation_results
import matplotlib.pyplot as plt

config = SimulationConfig()
config.barrier_type = "vertical"
config.steps = 100

pop, env, bar, col = run_simulation(config)
plot_simulation_results(col, bar, config)
plt.savefig("moja_symulacja.png")
```

### Test 2: Porównanie
```python
from symulacja import SimulationConfig, run_simulation

configs = {
    'z_barierą': 'vertical',
    'bez_bariery': 'none',
}

for name, barrier_type in configs.items():
    config = SimulationConfig()
    config.barrier_type = barrier_type
    config.steps = 150
    
    pop, env, bar, col = run_simulation(config, verbose=False)
    final = col.stats[-1]
    
    print(f"{name}: diversity = {final.genetic_diversity:.4f}")
```

### Test 3: Analiza Parametru
```python
from symulacja import SimulationConfig, run_simulation

mutations = [0.01, 0.02, 0.05]

for mut in mutations:
    config = SimulationConfig()
    config.p_mutation = mut
    
    pop, env, bar, col = run_simulation(config, verbose=False)
    final = col.stats[-1]
    
    print(f"Mutacja {mut}: diversity = {final.genetic_diversity:.4f}")
```

---

## Linki do Dokumentacji

- **[README.md](https://github.com/akotu235/species-formation-simulation/blob/master/README.md)** - Pełna dokumentacja techniczna
- **[DOKUMENTACJA_NAUKOWA.md](https://github.com/akotu235/species-formation-simulation/blob/master/DOKUMENTACJA_NAUKOWA.md)** - Biologia i matematyka
- **[config_gallery.py](https://github.com/akotu235/species-formation-simulation/blob/master/config_gallery.py)** - Przykłady konfiguracji

---

**Powodzenia w eksperymentach!** 🧬
