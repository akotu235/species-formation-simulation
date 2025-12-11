#!/usr/bin/env python3
"""
SZYBKI START - Symulacja Formowania Się Gatunków
=================================================

Ten skrypt pokazuje jak używać modułu symulacji w prosty sposób.
"""

from symulacja import run_simulation, visualize_comparison, analyze_genetic_divergence
import matplotlib.pyplot as plt
import numpy as np


def example_1_basic_simulation():
    """Przykład 1: Podstawowa symulacja z barierą"""
    print("\n" + "="*60)
    print("PRZYKŁAD 1: Podstawowa symulacja z barierą")
    print("="*60)
    
    config = {
        'grid_size': 20,
        'initial_pop_size': 150,
        'generations': 100,
        'mutation_rate': 0.05,
        'barrier_type': 'vertical',
    }
    
    print(f"Parametry:")
    print(f"  - Rozmiar gridu: {config['grid_size']}x{config['grid_size']}")
    print(f"  - Populacja początkowa: {config['initial_pop_size']}")
    print(f"  - Generacji: {config['generations']}")
    print(f"  - Typ bariery: {config['barrier_type']}")
    
    print("\nUruchamianie symulacji...")
    populations, env, barriers, collection = run_simulation(config)
    
    print(f"Zakończono!")
    print(f"  - Końcowa populacja: {collection['total_population'][-1]}")
    print(f"  - Końcowa różnorodność: {collection['genetic_diversity'][-1]:.4f}")
    
    # Wizualizacja
    visualize_comparison(populations, env, barriers, collection, 
                        "Przykład 1: Symulacja z barierą pionową",
                        "results/example1_barrier.png")
    print("\nZapisano: results/example1_barrier.png\n")


def example_2_no_barrier():
    """Przykład 2: Symulacja bez bariery - dla porównania"""
    print("\n" + "="*60)
    print("PRZYKŁAD 2: Symulacja bez bariery (porównanie)")
    print("="*60)
    
    config = {
        'grid_size': 20,
        'initial_pop_size': 150,
        'generations': 100,
        'mutation_rate': 0.05,
        'barrier_type': 'none',
    }
    
    print(f"Parametry: (bez bariery)")
    
    print("\nUruchamianie symulacji...")
    populations, env, barriers, collection = run_simulation(config)
    
    print(f"Zakończono!")
    print(f"  - Końcowa populacja: {collection['total_population'][-1]}")
    print(f"  - Końcowa różnorodność: {collection['genetic_diversity'][-1]:.4f}")
    
    # Wizualizacja
    visualize_comparison(populations, env, barriers, collection, 
                        "Przykład 2: Symulacja bez bariery",
                        "results/example2_no_barrier.png")
    print("\nZapisano: results/example2_no_barrier.png\n")


def example_3_horizontal_barrier():
    """Przykład 3: Bariera pozioma"""
    print("\n" + "="*60)
    print("PRZYKŁAD 3: Bariera pozioma")
    print("="*60)
    
    config = {
        'grid_size': 20,
        'initial_pop_size': 150,
        'generations': 100,
        'mutation_rate': 0.05,
        'barrier_type': 'horizontal',
    }
    
    print(f"Parametry: (bariera pozioma)")
    
    print("\nUruchamianie symulacji...")
    populations, env, barriers, collection = run_simulation(config)
    
    print(f"Zakończono!")
    print(f"  - Końcowa populacja: {collection['total_population'][-1]}")
    print(f"  - Końcowa różnorodność: {collection['genetic_diversity'][-1]:.4f}")
    
    # Wizualizacja
    visualize_comparison(populations, env, barriers, collection, 
                        "Przykład 3: Bariera pozioma",
                        "results/example3_horizontal.png")
    print("\nZapisano: results/example3_horizontal.png\n")


def example_4_mutation_sensitivity():
    """Przykład 4: Wpływ tempa mutacji"""
    print("\n" + "="*60)
    print("PRZYKŁAD 4: Wpływ tempa mutacji")
    print("="*60)
    
    mutation_rates = [0.01, 0.05, 0.10]
    results = {}
    
    for mut_rate in mutation_rates:
        print(f"\nUruchamianie z mutation_rate={mut_rate}...")
        
        config = {
            'grid_size': 15,
            'initial_pop_size': 100,
            'generations': 80,
            'mutation_rate': mut_rate,
            'barrier_type': 'vertical',
        }
        
        populations, env, barriers, collection = run_simulation(config)
        results[mut_rate] = collection
        
        final_div = collection['genetic_diversity'][-1]
        print(f"  ✓ Końcowa różnorodność: {final_div:.4f}")
    
    # Porównanie na jednym wykresie
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle('Przykład 4: Wpływ tempa mutacji na dynamikę populacji', 
                 fontsize=14, fontweight='bold')
    
    for idx, (mut_rate, collection) in enumerate(results.items()):
        ax = axes[idx]
        
        generations = range(len(collection['total_population']))
        
        # Wykres 1: Populacja
        ax_pop = ax
        ax_pop.plot(generations, collection['total_population'], 'b-', linewidth=2, label='Populacja')
        ax_pop.set_xlabel('Generacja')
        ax_pop.set_ylabel('Liczba osobników', color='b')
        ax_pop.tick_params(axis='y', labelcolor='b')
        ax_pop.set_title(f'Mutation Rate = {mut_rate}')
        ax_pop.grid(True, alpha=0.3)
        
        # Wykres 2: Różnorodność (na drugiej osi Y)
        ax_div = ax_pop.twinx()
        ax_div.plot(generations, collection['genetic_diversity'], 'r-', linewidth=2, label='Różnorodność')
        ax_div.set_ylabel('Różnorodność genetyczna', color='r')
        ax_div.tick_params(axis='y', labelcolor='r')
    
    plt.tight_layout()
    plt.savefig('results/example4_mutation.png', dpi=100)
    print("\nZapisano: results/example4_mutation.png\n")
    
    # Podsumowanie
    print("\n" + "="*60)
    print("PODSUMOWANIE")
    print("="*60)
    for mut_rate, collection in results.items():
        final_pop = collection['total_population'][-1]
        final_div = collection['genetic_diversity'][-1]
        print(f"Mutation {mut_rate:4.2f}: Population={final_pop:3d}, Diversity={final_div:.4f}")


def example_5_population_size_impact():
    """Przykład 5: Wpływ wielkości populacji początkowej"""
    print("\n" + "="*60)
    print("PRZYKŁAD 5: Wpływ wielkości populacji początkowej")
    print("="*60)
    
    pop_sizes = [50, 100, 200]
    results = {}
    
    for pop_size in pop_sizes:
        print(f"\nUruchamianie z initial_pop_size={pop_size}...")
        
        config = {
            'grid_size': 15,
            'initial_pop_size': pop_size,
            'generations': 80,
            'mutation_rate': 0.05,
            'barrier_type': 'vertical',
        }
        
        populations, env, barriers, collection = run_simulation(config)
        results[pop_size] = collection
        
        final_div = collection['genetic_diversity'][-1]
        divergence = analyze_genetic_divergence(populations) if len(populations) > 1 else 0
        print(f"  ✓ Końcowa różnorodność: {final_div:.4f}")
        print(f"  ✓ Dywergencja między populacjami: {divergence:.4f}")
    
    # Porównanie na jednym wykresie
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle('Przykład 5: Wpływ wielkości populacji', 
                 fontsize=14, fontweight='bold')
    
    # Wykres 1: Dynamika populacji
    ax1 = axes[0]
    colors = ['blue', 'green', 'red']
    for (pop_size, collection), color in zip(results.items(), colors):
        ax1.plot(collection['total_population'], label=f'Pop_init={pop_size}', 
                color=color, linewidth=2)
    ax1.set_xlabel('Generacja')
    ax1.set_ylabel('Liczba osobników')
    ax1.set_title('Dynamika populacji')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Wykres 2: Różnorodność genetyczna
    ax2 = axes[1]
    for (pop_size, collection), color in zip(results.items(), colors):
        ax2.plot(collection['genetic_diversity'], label=f'Pop_init={pop_size}', 
                color=color, linewidth=2)
    ax2.set_xlabel('Generacja')
    ax2.set_ylabel('Różnorodność genetyczna')
    ax2.set_title('Ewolucja różnorodności')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/example5_population_size.png', dpi=100)
    print("\nZapisano: results/example5_population_size.png\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("SZYBKI START - 5 PRAKTYCZNYCH PRZYKŁADÓW")
    print("="*60)
    print("\nTen skrypt demonstruje podstawowe możliwości symulacji")
    print("formowania się gatunków z barierami geograficznymi.")
    
    # Uruchom wszystkie przykłady
    example_1_basic_simulation()
    example_2_no_barrier()
    example_3_horizontal_barrier()
    example_4_mutation_sensitivity()
    example_5_population_size_impact()
    
    print("\n" + "="*60)
    print("WSZYSTKIE PRZYKŁADY ZAKOŃCZONE")
    print("="*60)
    print("\nWygenerowane pliki:")
    print("  • example1_barrier.png")
    print("  • example2_no_barrier.png")
    print("  • example3_horizontal.png")
    print("  • example4_mutation.png")
    print("  • example5_population_size.png")
    print("\nSzczegóły w: README.md i KARTA_SZYBKIEGO_DOSTĘPU.md")
