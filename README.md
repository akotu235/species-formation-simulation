# Symulacja Formowania Się Gatunków w Warunkach Barier Geograficznych

## Przegląd

Ta symulacja modeluje proces formowania się gatunków (specjacji) w populacjach organizmów w obecności barier geograficznych. Symulacja implementuje:

- **Dynamikę populacji**: migracja, rozród, mutacje
- **Selekcję naturalną**: dopasowanie do lokalnego środowiska
- **Bariery geograficzne**: izolacja genetyczna populacji
- **Zbieranie danych**: śledzenie zmian genetycznych w czasie
- **Analizę**: detekcja divergencji genetycznej i specjacji

## Struktura Projektu

```
projekt/
├── symulacja.py              # Główny moduł z logiką symulacji
├── run_simulations.py        # Skrypt do uruchamiania wielowariantowych eksperymentów
├── README.md                 # Ten plik
└── [wygenerowane wyniki]/
    ├── snapshot_final.png    # Snapshota stanu końcowego
    ├── results_barrier.png   # Wykresy wyników (z barierą)
    ├── results_no_barrier.png # Wykresy wyników (bez bariery)
    └── ...
```

## Komponenty Symulacji

### 1. Model Genetyki
- **Genotyp**: wektor 8 alleli (wartości 0-2)
- **Fitness**: funkcja dopasowania do lokalnego środowiska
  - `fitness = 1 / (1 + |suma_genów - 2*env_value|)`
- **Mutacje**: losowa zmiana alleli z częstością ~2%

### 2. Dynamika Przestrzenna
- **Siatka 2D**: 50×50 komórek
- **Sąsiedztwo**: von Neumann (4 sąsiedzi)
- **Bariery**: uniemożliwiają migrację między regionami
- **Pojemność**: max 25 osobników na komórkę

### 3. Procesy Ewolucyjne
- **Migracja** (~15%): losowe przemieszczanie się do sąsiednich komórek
- **Rozród** (bazowe ~12%, zależy od fitness): rozmnażanie się osobników
- **Selekcja**: osobniki lepiej dostosowane mają wyższe szanse rozrodu
- **Regulacja liczebności**: w każdej komórce limit populacji

### 4. Zbieranie Danych
Dla każdego kroku symulacji zbierane są:
- **population_size**: liczba żywych osobników
- **mean_fitness**: średnie dopasowanie do środowiska
- **genetic_diversity**: różnorodność genetyczna (odległość Hamminga)
- **left_pop_size**: liczba osobników po lewej stronie bariery
- **right_pop_size**: liczba osobników po prawej stronie bariery

## Konfiguracja Parametrów

### Domyślna Konfiguracja
```python
config = SimulationConfig()
config.height = 50              # Wysokość siatki
config.width = 50               # Szerokość siatki
config.num_individuals = 300    # Liczba osobników na starcie
config.genome_length = 8        # Długość genotypu
config.steps = 200              # Liczba kroków symulacji

config.p_mutation = 0.02        # Prawdopodobieństwo mutacji
config.p_migration = 0.15       # Prawdopodobieństwo migracji
config.p_base_repro = 0.12      # Bazowe prawdopodobieństwo rozrodu
config.max_per_cell = 25        # Max osobników w komórce

config.barrier_type = "vertical" # "vertical", "horizontal", "none"
```

### Typy Barier
- **"vertical"**: pionowa bariera w środku siatki (dzieli populację na lewą i prawą)
- **"horizontal"**: pozioma bariera w środku siatki (dzieli populację na górną i dolną)
- **"none"**: brak barier (symulacja kontrolna)

## Uruchamianie Symulacji

### Podstawowe uruchomienie (główny skrypt)
```bash
python3 symulacja.py
```

Uruchamia dwa warianty:
1. Symulacja z pionową barierą
2. Symulacja bez bariery (kontrola)

### Wielowariantowe eksperymenty
```bash
python3 run_simulations.py
```

Uruchamia 3 eksperymenty:
1. **Eksperyment 1**: Porównanie z barierą vs bez bariery
2. **Eksperyment 2**: Wpływ szybkości mutacji
3. **Eksperyment 3**: Wpływ wielkości populacji

Lub konkretny eksperyment:
```bash
python3 run_simulations.py 1  # Tylko eksperyment 1
python3 run_simulations.py 2  # Tylko eksperyment 2
python3 run_simulations.py 3  # Tylko eksperyment 3
```

## Interpretacja Wyników

### Snapshota stanu (snapshot_final.png)
- **Lewy panel**: Rozmieszczenie populacji na siatce
  - Kolor osobników: średni genotyp (niski = czerwony, wysoki = niebieski)
  - Czerwone kwadraty: bariery geograficzne
  - Kolor tła: wartość środowiska (ciemny = niska, jasny = wysoka)
- **Prawy panel**: Histogram rozkładu alleli

### Wykresy wyników (results_barrier.png, results_no_barrier.png)

#### 1. Dynamika liczebności populacji
- **Niebieska linia**: całkowita liczba osobników
- **Czerwona linia przerywana**: populacja po lewej stronie bariery
- **Zielona linia przerywana**: populacja po prawej stronie bariery

Interpretacja:
- Z barierą: populacje mogą rozbiegać się do różnych wielkości
- Bez bariery: populacja pozostaje bardziej jednorodna

#### 2. Ewolucja dopasowania
- Wyższa wartość = lepsze przystosowanie do środowiska
- Oczekiwany trend: szybki wzrost, następnie stabilizacja

#### 3. Zmienność genetyczna (genetic diversity)
- Mierzy się jako średnia odległość Hamminga między osobnikami
- Wyższa wartość = większa różnorodność
- **Z barierą**: zwykle maleje szybciej (izolacja prowadzi do utraty zmienności)
- **Bez bariery**: zmienność pozostaje wyższa (gene flow utrzymuje zmienność)

#### 4. Rozkład populacji względem bariery
- Pokazuje, czy populacje po obu stronach bariery mogą niezależnie rośnie
- **Silna specjacja**: populacje znacznie się różnią w wielkości

## Miary Specjacji

### Divergencja Genetyczna
```
genetic_distance = średnia(|mean_left_genotype - mean_right_genotype|)
```
- Wartości bliskie 0: populacje genetycznie podobne
- Wartości bliskie 1: populacje genetycznie divergentne (specjacja)

### Różnorodność Genetyczna
```
genetic_diversity = średnia(distance Hamminga między wszystkimi parami)
```
- Wskazuje na ilość zmienności w populacji
- Bariera redukuje wewnątrz-populacyjną zmienność
- Ale zwiększa między-populacyjną divergencję

## Oczekiwane Wyniki

### Z Barierą
✓ Dwie izolowane sub-populacje  
✓ Różne alele frecjonują w każdej populacji  
✓ Wyższa divergencja genetyczna między populacjami  
✓ Niższa wewnętrzna zmienność (w każdej populacji)  
✓ Ewolucja w różnych kierunkach (szansa na specjację)  

### Bez Bariery
✓ Jedna jednolita populacja  
✓ Continuos gene flow między regionami  
✓ Niska divergencja genetyczna  
✓ Wyższa wewnętrzna zmienność  
✓ Brak specjacji  

## Biologiczna Interpretacja

Ta symulacja modeluje procesy rzeczywiste obserwowane w naturze:

1. **Geograficzne izolowanie**: bariery fizyczne uniemożliwiają migrację
2. **Adaptacja lokalna**: każda populacja dostosowuje się do swojego środowiska
3. **Genetyczne wkluczenie**: brak gene flow prowadzi do akumulacji różnic
4. **Specjacja**: po wystarczająco długim okresie izolacji, populacje mogą stać się niekompatybilne reprodukcyjnie
5. **Biodiversity**: bariery są kluczowe dla utrzymania różnorodności biologicznej

## Rozszerzenia Modelu

Możliwe ulepszenia i rozszerzenia:

1. **Złożone bariery**: mosaikowe bariery, bariery zmieniające się w czasie
2. **Selekcja dyploidalna**: genotypy diploidalne, dominacja/recesywność
3. **Migracja asymetryczna**: różne kierunki migracji
4. **Zmienne środowisko**: parametry środowiska zmieniające się w czasie
5. **Interakcje międzygatunkowe**: konkurencja, drapieżnictwo, symbioza
6. **Seksualne dobór**: preferencje u partnera
7. **Śledzenie genealogii**: drzewa filogenetyczne populacji

## Wymagane Biblioteki

```
numpy
matplotlib
scipy
```

Instalacja:
```bash
pip install numpy matplotlib scipy
```

## Pliki Wyjściowe

- `snapshot_final.png`: Vizualizacja stanu końcowego symulacji
- `results_barrier.png`: Wykresy metryki dla symulacji z barierą
- `results_no_barrier.png`: Wykresy metryki dla symulacji bez bariery
- `exp1_comparison.png`: Porównanie trzech wariantów barier
- `exp2_mutation_sensitivity.png`: Wpływ szybkości mutacji
- `exp3_population_size.png`: Wpływ wielkości populacji

## Referencje

Simulation implements concepts from:

- **Allopatric Speciation**: Geographic isolation leading to reproductive isolation
- **Microgeographic Differentiation**: Adaptation to local environmental variation
- **Neutral Evolution**: Genetic drift in isolated populations
- **Adaptive Evolution**: Selection based on fitness to environment

## Autorzy projektu

**Projekt zaliczeniowy:** Modelowanie i Symulacja Systemów

**Temat:** Formowanie się gatunków w warunkach barier geograficznych

**Autorzy:**
  * Izabela Bubula
  * [Andrzej Kotulski](https://akotu235.github.io)

