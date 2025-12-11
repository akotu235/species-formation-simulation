#!/usr/bin/env python3
"""
Predefiniowane Konfiguracje Symulacji
=====================================

Ten plik zawiera gotowe konfiguracje do różnych scenariuszy badawczych.
Wykorzystuje słowniki zamiast obiektów klasy SimulationConfig.
"""

import os
from symulacja import run_simulation, visualize_comparison, analyze_genetic_divergence, ensure_results_directory
import numpy as np
import matplotlib.pyplot as plt


# ============================================================================
# PREDEFINIOWANE KONFIGURACJE (SŁOWNIKI)
# ============================================================================

def config_default():
    """Konfiguracja domyślna (standardowa)"""
    return {
        'grid_size': 20,
        'initial_pop_size': 150,
        'generations': 150,
        'mutation_rate': 0.05,
        'barrier_type': 'vertical',
    }


def config_weak_barrier():
    """Słaba bariera - wysoka migracja"""
    return {
        'grid_size': 20,
        'initial_pop_size': 150,
        'generations': 150,
        'mutation_rate': 0.02,
        'barrier_type': 'vertical',
    }


def config_strong_barrier():
    """Silna bariera - niska migracja"""
    return {
        'grid_size': 20,
        'initial_pop_size': 100,
        'generations': 150,
        'mutation_rate': 0.10,
        'barrier_type': 'vertical',
    }


def config_high_mutation():
    """Wysoka mutacyjność - szybka ewolucja"""
    return {
        'grid_size': 15,
        'initial_pop_size': 100,
        'generations': 100,
        'mutation_rate': 0.10,
        'barrier_type': 'vertical',
    }


def config_low_mutation():
    """Niska mutacyjność - wolna ewolucja"""
    return {
        'grid_size': 15,
        'initial_pop_size': 100,
        'generations': 150,
        'mutation_rate': 0.01,
        'barrier_type': 'vertical',
    }


def config_small_population():
    """Mała populacja - silny drif genetyczny"""
    return {
        'grid_size': 15,
        'initial_pop_size': 50,
        'generations': 150,
        'mutation_rate': 0.05,
        'barrier_type': 'vertical',
    }


def config_large_population():
    """Duża populacja - słaby drif genetyczny"""
    return {
        'grid_size': 25,
        'initial_pop_size': 300,
        'generations': 150,
        'mutation_rate': 0.05,
        'barrier_type': 'vertical',
    }


def config_no_barrier():
    """Brak bariery - kontrola"""
    return {
        'grid_size': 20,
        'initial_pop_size': 150,
        'generations': 150,
        'mutation_rate': 0.05,
        'barrier_type': 'none',
    }


def config_horizontal_barrier():
    """Bariera pozioma"""
    return {
        'grid_size': 20,
        'initial_pop_size': 150,
        'generations': 150,
        'mutation_rate': 0.05,
        'barrier_type': 'horizontal',
    }


def config_short_term():
    """Krótkoterminowa symulacja"""
    return {
        'grid_size': 15,
        'initial_pop_size': 100,
        'generations': 50,
        'mutation_rate': 0.05,
        'barrier_type': 'vertical',
    }


def config_long_term():
    """Długoterminowa symulacja"""
    return {
        'grid_size': 20,
        'initial_pop_size': 150,
        'generations': 300,
        'mutation_rate': 0.05,
        'barrier_type': 'vertical',
    }


def config_extreme_isolation():
    """Ekstremalna izolacja - najszybsza specjacja"""
    return {
        'grid_size': 15,
        'initial_pop_size': 50,
        'generations': 200,
        'mutation_rate': 0.08,
        'barrier_type': 'vertical',
    }


def config_gene_flow_dominated():
    """Gene flow dominujący - brak specjacji"""
    return {
        'grid_size': 25,
        'initial_pop_size': 300,
        'generations': 150,
        'mutation_rate': 0.02,
        'barrier_type': 'none',
    }


# ============================================================================
# GALERIA KONFIGURACJI
# ============================================================================

class ConfigGallery:
    """Galeria predefiniowanych konfiguracji"""
    
    configs = {
        'default': config_default,
        'weak_barrier': config_weak_barrier,
        'strong_barrier': config_strong_barrier,
        'high_mutation': config_high_mutation,
        'low_mutation': config_low_mutation,
        'small_pop': config_small_population,
        'large_pop': config_large_population,
        'no_barrier': config_no_barrier,
        'horizontal': config_horizontal_barrier,
        'short_term': config_short_term,
        'long_term': config_long_term,
        'extreme': config_extreme_isolation,
        'gene_flow': config_gene_flow_dominated,
    }
    
    @classmethod
    def get(cls, name):
        """Pobierz konfigurację po nazwie"""
        if name not in cls.configs:
            raise ValueError(f"Nieznana konfiguracja: {name}\nDostępne: {list(cls.configs.keys())}")
        return cls.configs[name]()
    
    @classmethod
    def list_all(cls):
        """Wylistuj wszystkie dostępne konfiguracje"""
        return list(cls.configs.keys())
    
    @classmethod
    def describe(cls, name):
        """Opis konfiguracji"""
        descriptions = {
            'default': 'Konfiguracja domyślna',
            'weak_barrier': 'Słaba bariera - wysoka migracja',
            'strong_barrier': 'Silna bariera - niska migracja',
            'high_mutation': 'Wysoka mutacyjność',
            'low_mutation': 'Niska mutacyjność',
            'small_pop': 'Mała populacja',
            'large_pop': 'Duża populacja',
            'no_barrier': 'Brak bariery',
            'horizontal': 'Bariera pozioma',
            'short_term': 'Krótka symulacja',
            'long_term': 'Długa symulacja',
            'extreme': 'Ekstremalna izolacja',
            'gene_flow': 'Gene flow dominujący',
        }
        return descriptions.get(name, 'Brak opisu')


# ============================================================================
# FUNKCJE DEMONSTRACYJNE
# ============================================================================

def demo_compare_configs(config_names):
    """Porównaj wyniki różnych konfiguracji"""
    print(f"\nPorównanie konfiguracji: {config_names}")
    print("=" * 70)
    
    results = {}
    
    for name in config_names:
        try:
            print(f"  [{name}] ", end='', flush=True)
            config = ConfigGallery.get(name)
            populations, env, barriers, collection = run_simulation(config)
            results[name] = {
                'config': config,
                'populations': populations,
                'env': env,
                'barriers': barriers,
                'collection': collection,
            }
            
            final_pop = collection['total_population'][-1] if collection['total_population'] else 0
            final_div = collection['genetic_diversity'][-1] if collection['genetic_diversity'] else 0
            divergence = analyze_genetic_divergence(populations) if len(populations) > 1 else 0
            
            print(f"✓ Pop={final_pop}, Div={final_div:.4f}, Divergence={divergence:.4f}")
        except Exception as e:
            print(f"✗ Błąd: {e}")
    
    # Wizualizacja wyników
    if results:
        fig, axes = plt.subplots(len(results), 1, figsize=(12, 4 * len(results)))
        if len(results) == 1:
            axes = [axes]
        
        for idx, (name, data) in enumerate(results.items()):
            ax = axes[idx]
            collection = data['collection']
            generations = range(len(collection['total_population']))
            
            ax2 = ax.twinx()
            
            ax.plot(generations, collection['total_population'], 'b-', linewidth=2.5, label='Populacja')
            ax2.plot(generations, collection['genetic_diversity'], 'r-', linewidth=2.5, label='Różnorodność')
            
            ax.set_xlabel('Generacja')
            ax.set_ylabel('Liczba osobników', color='b')
            ax2.set_ylabel('Różnorodność genetyczna', color='r')
            ax.set_title(f'Konfiguracja: {name} - {ConfigGallery.describe(name)}', fontweight='bold')
            ax.tick_params(axis='y', labelcolor='b')
            ax2.tick_params(axis='y', labelcolor='r')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/config_comparison.png', dpi=100)
        print("\n✓ Zapisano: results/config_comparison.png")


def demo_barrier_types():
    """Pokaz różnych typów barier"""
    print("\nDemo typów barier...")
    
    barrier_types = ['vertical', 'horizontal', 'none']
    results = {}
    
    for barrier_type in barrier_types:
        print(f"  [{barrier_type}] ", end='', flush=True)
        
        config = {
            'grid_size': 20,
            'initial_pop_size': 150,
            'generations': 120,
            'mutation_rate': 0.05,
            'barrier_type': barrier_type,
        }
        
        populations, env, barriers, collection = run_simulation(config)
        results[barrier_type] = (populations, env, barriers, collection)
        
        divergence = analyze_genetic_divergence(populations) if len(populations) > 1 else 0
        print(f"✓ Divergence={divergence:.4f}")
    
    # Wizualizacja
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, (barrier_type, (populations, env, barriers, collection)) in enumerate(results.items()):
        ax = axes[idx]
        generations = range(len(collection['genetic_diversity']))
        
        ax.plot(generations, collection['genetic_diversity'], 'b-', linewidth=2.5)
        ax.fill_between(generations, collection['genetic_diversity'], alpha=0.3)
        ax.set_xlabel('Generacja')
        ax.set_ylabel('Różnorodność genetyczna')
        ax.set_title(f'Typ bariery: {barrier_type.upper()}', fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/barrier_types_demo.png', dpi=100)
    print("✓ Zapisano: results/barrier_types_demo.png")


def demo_population_sensitivity():
    """Pokaz wrażliwości na wielkość populacji"""
    print("\nDemo wrażliwości na wielkość populacji...")
    
    pop_sizes = [50, 150, 300]
    results = {}
    
    for pop_size in pop_sizes:
        print(f"  [pop={pop_size}] ", end='', flush=True)
        
        config = {
            'grid_size': 20,
            'initial_pop_size': pop_size,
            'generations': 150,
            'mutation_rate': 0.05,
            'barrier_type': 'vertical',
        }
        
        populations, env, barriers, collection = run_simulation(config)
        results[pop_size] = (populations, env, barriers, collection)
        print("✓")
    
    # Wizualizacja
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, (pop_size, (populations, env, barriers, collection)) in enumerate(results.items()):
        ax = axes[idx]
        generations = range(len(collection['genetic_diversity']))
        
        ax.plot(generations, collection['genetic_diversity'], 'b-', linewidth=2.5)
        ax.fill_between(generations, collection['genetic_diversity'], alpha=0.3)
        ax.set_xlabel('Generacja')
        ax.set_ylabel('Różnorodność genetyczna')
        ax.set_title(f'Populacja początkowa: {pop_size}', fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/population_sensitivity_demo.png', dpi=100)
    print("✓ Zapisano: results/population_sensitivity_demo.png")


# ============================================================================
# MAIN - URUCHAMIANIE DEMO
# ============================================================================

if __name__ == "__main__":
    # Stwórz katalog results jeśli nie istnieje
    ensure_results_directory()
    
    print("\n" + "=" * 70)
    print("GALERIA PREDEFINIOWANYCH KONFIGURACJI")
    print("=" * 70)
    
    # Wypisz dostępne konfiguracje
    print("\nDostępne konfiguracje:")
    for i, name in enumerate(ConfigGallery.list_all(), 1):
        desc = ConfigGallery.describe(name)
        print(f"  {i:2d}. {name:20s} - {desc}")
    
    # Demo 1: Porównanie wybranych konfiguracji
    print("\n" + "=" * 70)
    print("DEMO 1: Porównanie wybranych konfiguracji")
    print("=" * 70)
    demo_compare_configs(['default', 'weak_barrier', 'strong_barrier'])
    
    # Demo 2: Typy barier
    print("\n" + "=" * 70)
    print("DEMO 2: Porównanie typów barier")
    print("=" * 70)
    demo_barrier_types()
    
    # Demo 3: Wrażliwość na populację
    print("\n" + "=" * 70)
    print("DEMO 3: Wrażliwość na wielkość populacji")
    print("=" * 70)
    demo_population_sensitivity()
    
    print("\n" + "=" * 70)
    print("DEMO ZAKOŃCZONE")
    print("=" * 70)
    print("\nWygenerowane pliki:")
    print("  • config_comparison.png")
    print("  • barrier_types_demo.png")
    print("  • population_sensitivity_demo.png")
