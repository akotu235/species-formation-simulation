#!/usr/bin/env python3
"""
Skrypt do uruchamiania różnych wariantów symulacji formowania się gatunków.
Umożliwia łatwe testowanie różnych parametrów i scenariuszy.
"""

import sys
import os
sys.path.insert(0, '/home/andrzej/Studia/Modelowanie i symulacja systemów/projekt')

from symulacja import run_simulation, analyze_genetic_divergence, visualize_comparison, ensure_results_directory
import matplotlib.pyplot as plt


def ensure_results_dir():
    """Tworzy katalog results jeśli nie istnieje"""
    if not os.path.exists('results'):
        os.makedirs('results')


def run_barrier_vs_no_barrier_comparison():
    """Eksperyment 1: Porównanie z barierą vs bez bariery"""
    print("\n" + "="*70)
    print("EKSPERYMENT 1: WPŁYW BARIERY NA SPECJACJĘ")
    print("="*70)
    
    # Konfiguracja 1: Z PIONOWĄ BARIERĄ
    config1 = {
        'grid_size': 10,
        'initial_pop_size': 100,
        'generations': 150,
        'mutation_rate': 0.05,
        'barrier_type': 'vertical',
        'barrier_position': 5,
    }
    
    print("\n[1/3] Symulacja Z PIONOWĄ BARIERĄ...")
    print(f"  - Wymiary: {config1['grid_size']}x{config1['grid_size']}")
    print(f"  - Populacja początkowa: {config1['initial_pop_size']}")
    print(f"  - Generacji: {config1['generations']}")
    print(f"  - Bariera: pionowa na kolumnie {config1['barrier_position']}")
    pop1, env1, bar1, col1 = run_simulation(config1)
    print("  ✓ Zakończono")
    
    # Konfiguracja 2: BEZ BARIERY
    config2 = {
        'grid_size': 10,
        'initial_pop_size': 100,
        'generations': 150,
        'mutation_rate': 0.05,
        'barrier_type': 'none',
    }
    
    print("\n[2/3] Symulacja BEZ BARIERY...")
    print(f"  - Wymiary: {config2['grid_size']}x{config2['grid_size']}")
    print(f"  - Populacja początkowa: {config2['initial_pop_size']}")
    print(f"  - Generacji: {config2['generations']}")
    print(f"  - Bariera: brak")
    pop2, env2, bar2, col2 = run_simulation(config2)
    print("  ✓ Zakończono")
    
    # ANALIZA
    print("\n[3/3] Analiza wyników...")
    div1 = analyze_genetic_divergence(pop1)
    div2 = analyze_genetic_divergence(pop2)
    
    print("\n" + "-"*70)
    print("WYNIKI EKSPERYMENTU 1")
    print("-"*70)
    print(f"\nZ PIONOWĄ BARIERĄ:")
    print(f"  - Liczba populacji: {len(pop1)}")
    print(f"  - Łączna populacja: {sum(len(p) for p in pop1)}")
    print(f"  - Średnia divergencja genetyczna: {div1:.4f}")
    print(f"  - Diagnoza: {'✓ SPECJACJA' if div1 > 0.25 else '✗ Brak specjacji'}")
    
    print(f"\nBEZ BARIERY:")
    print(f"  - Liczba populacji: {len(pop2)}")
    print(f"  - Łączna populacja: {sum(len(p) for p in pop2)}")
    print(f"  - Średnia divergencja genetyczna: {div2:.4f}")
    print(f"  - Diagnoza: {'✓ SPECJACJA' if div2 > 0.25 else '✗ Brak specjacji'}")
    
    print(f"\nROZNICA: {div1 - div2:.4f}")
    print(f"Wnioski: Bariera {'PRZYSPIESZA' if div1 > div2 * 1.5 else 'nie wpływa na'} specjację")
    
    # Wizualizacja
    visualize_comparison(pop1, env1, bar1, col1, "Z PIONOWĄ BARIERĄ", "results/results_barrier.png")
    visualize_comparison(pop2, env2, bar2, col2, "BEZ BARIERY", "results/results_no_barrier.png")
    print("\n✓ Wykresy zapisane: results/results_barrier.png, results/results_no_barrier.png")


def run_mutation_rate_experiment():
    """Eksperyment 2: Wpływ szybkości mutacji"""
    print("\n" + "="*70)
    print("EKSPERYMENT 2: WPŁYW SZYBKOŚCI MUTACJI")
    print("="*70)
    
    mutation_rates = [0.01, 0.05, 0.10]
    divergences = []
    populations = []
    
    for i, mut_rate in enumerate(mutation_rates, 1):
        config = {
            'grid_size': 10,
            'initial_pop_size': 80,
            'generations': 120,
            'mutation_rate': mut_rate,
            'barrier_type': 'vertical',
            'barrier_position': 5,
        }
        
        print(f"\n[{i}/{len(mutation_rates)}] Symulacja z mutation_rate={mut_rate}...")
        pop, env, bar, col = run_simulation(config)
        div = analyze_genetic_divergence(pop)
        
        divergences.append(div)
        populations.append(len(pop))
        
        print(f"  - Divergencja: {div:.4f}")
        print(f"  - Liczba populacji: {len(pop)}")
    
    print("\n" + "-"*70)
    print("WYNIKI EKSPERYMENTU 2")
    print("-"*70)
    for mut_rate, div, npop in zip(mutation_rates, divergences, populations):
        print(f"  Mutacja {mut_rate:5.2f}: divergencja={div:.4f}, populacje={npop}")
    
    # Wizualizacja
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    ax1.plot(mutation_rates, divergences, 'o-', linewidth=2, markersize=8, color='#2ecc71')
    ax1.set_xlabel('Szybkość mutacji', fontsize=11)
    ax1.set_ylabel('Divergencja genetyczna', fontsize=11)
    ax1.set_title('Wpływ mutacji na divergencję', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(mutation_rates, populations, 's-', linewidth=2, markersize=8, color='#3498db')
    ax2.set_xlabel('Szybkość mutacji', fontsize=11)
    ax2.set_ylabel('Liczba odrębnych populacji', fontsize=11)
    ax2.set_title('Wpływ mutacji na liczbę populacji', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/experiment2_mutation.png', dpi=150, bbox_inches='tight')
    print("\n✓ Wykres zapisany: results/experiment2_mutation.png")


def run_population_size_experiment():
    """Eksperyment 3: Wpływ wielkości populacji"""
    print("\n" + "="*70)
    print("EKSPERYMENT 3: WPŁYW WIELKOŚCI POPULACJI")
    print("="*70)
    
    pop_sizes = [50, 100, 200]
    divergences = []
    populations = []
    
    for i, pop_size in enumerate(pop_sizes, 1):
        config = {
            'grid_size': 10,
            'initial_pop_size': pop_size,
            'generations': 120,
            'mutation_rate': 0.05,
            'barrier_type': 'vertical',
            'barrier_position': 5,
        }
        
        print(f"\n[{i}/{len(pop_sizes)}] Symulacja z initial_pop_size={pop_size}...")
        pop, env, bar, col = run_simulation(config)
        div = analyze_genetic_divergence(pop)
        
        divergences.append(div)
        populations.append(len(pop))
        
        print(f"  - Divergencja: {div:.4f}")
        print(f"  - Liczba populacji: {len(pop)}")
    
    print("\n" + "-"*70)
    print("WYNIKI EKSPERYMENTU 3")
    print("-"*70)
    for pop_size, div, npop in zip(pop_sizes, divergences, populations):
        print(f"  Populacja {pop_size:3d}: divergencja={div:.4f}, populacje={npop}")
    
    # Wizualizacja
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    ax1.plot(pop_sizes, divergences, 'o-', linewidth=2, markersize=8, color='#e74c3c')
    ax1.set_xlabel('Wielkość populacji początkowej', fontsize=11)
    ax1.set_ylabel('Divergencja genetyczna', fontsize=11)
    ax1.set_title('Wpływ wielkości populacji na divergencję', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(pop_sizes, populations, 's-', linewidth=2, markersize=8, color='#9b59b6')
    ax2.set_xlabel('Wielkość populacji początkowej', fontsize=11)
    ax2.set_ylabel('Liczba odrębnych populacji', fontsize=11)
    ax2.set_title('Wpływ wielkości populacji na liczbę populacji', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/experiment3_population.png', dpi=150, bbox_inches='tight')
    print("\n✓ Wykres zapisany: results/experiment3_population.png")


if __name__ == '__main__':
    # Stwórz katalog results jeśli nie istnieje
    ensure_results_dir()
    
    print("\n" + "="*70)
    print("WIELOWARIANTOWA SYMULACJA FORMOWANIA SIĘ GATUNKÓW")
    print("="*70)
    print("\nRunning all experiments...")
    print("(Alternatywnie: python run_simulations.py [1|2|3])")
    
    if len(sys.argv) > 1:
        exp = sys.argv[1]
        if exp == '1':
            run_barrier_vs_no_barrier_comparison()
        elif exp == '2':
            run_mutation_rate_experiment()
        elif exp == '3':
            run_population_size_experiment()
        else:
            print(f"Nieznany eksperyment: {exp}")
    else:
        run_barrier_vs_no_barrier_comparison()
        run_mutation_rate_experiment()
        run_population_size_experiment()
    
    print("\n" + "="*70)
    print("✓ WSZYSTKIE EKSPERYMENTY ZAKOŃCZONE")
    print("="*70)
