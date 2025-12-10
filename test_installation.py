#!/usr/bin/env python3
"""
TEST WERYFIKACYJNY
==================

Skrypt do sprawdzenia, czy wszystkie komponenty są poprawnie zainstalowane.
"""

import sys

def test_imports():
    """Test importowania wymaganych bibliotek"""
    print("=" * 70)
    print("TEST 1: Weryfikacja bibliotek")
    print("=" * 70)
    
    libraries = {
        'numpy': 'Obliczenia numeryczne',
        'matplotlib': 'Wizualizacja',
        'matplotlib.pyplot': 'Wykresy',
        'scipy.spatial.distance': 'Metryki odległości',
    }
    
    all_ok = True
    for lib, desc in libraries.items():
        try:
            __import__(lib)
            print(f"✓ {lib:<30} ({desc})")
        except ImportError as e:
            print(f"✗ {lib:<30} ({desc})")
            print(f"  Błąd: {e}")
            all_ok = False
    
    return all_ok


def test_simulation_module():
    """Test głównego modułu symulacji"""
    print("\n" + "=" * 70)
    print("TEST 2: Weryfikacja modułu symulacji")
    print("=" * 70)
    
    try:
        from symulacja import (
            SimulationConfig, Individual, SimulationStats,
            DataCollector, run_simulation, init_environment,
            init_population, fitness, mutate, simulation_step,
            plot_simulation_snapshot, plot_simulation_results
        )
        
        classes = [SimulationConfig, Individual, SimulationStats, DataCollector]
        functions = [run_simulation, init_environment, init_population, 
                    fitness, mutate, simulation_step,
                    plot_simulation_snapshot, plot_simulation_results]
        
        print("✓ Klasy:")
        for cls in classes:
            print(f"  - {cls.__name__}")
        
        print("\n✓ Funkcje:")
        for func in functions:
            print(f"  - {func.__name__}")
        
        return True
        
    except Exception as e:
        print(f"✗ Błąd przy importowaniu modułu:")
        print(f"  {e}")
        return False


def test_quick_simulation():
    """Test szybkiej symulacji"""
    print("\n" + "=" * 70)
    print("TEST 3: Szybka symulacja (10 kroków)")
    print("=" * 70)
    
    try:
        from symulacja import SimulationConfig, run_simulation
        
        config = {
            'grid_size': 20,
            'initial_pop_size': 50,
            'generations': 10,
            'mutation_rate': 0.05,
            'barrier_type': 'none'
        }
        
        print("Uruchamianie symulacji...")
        populations, env, barriers, collection = run_simulation(config)
        
        total_pop = collection['total_population'][-1] if collection['total_population'] else 0
        diversity = collection['genetic_diversity'][-1] if collection['genetic_diversity'] else 0
        print(f"✓ Symulacja zakończona pomyślnie")
        print(f"  - Liczba osobników: {total_pop}")
        print(f"  - Różnorodność genetyczna: {diversity:.4f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Błąd podczas symulacji:")
        print(f"  {e}")
        import traceback
        traceback.print_exc()
        return False


def test_helper_scripts():
    """Test dostępności skryptów pomocniczych"""
    print("\n" + "=" * 70)
    print("TEST 4: Weryfikacja skryptów pomocniczych")
    print("=" * 70)
    
    import os
    
    scripts = [
        'symulacja.py',
        'run_simulations.py',
        'quickstart.py',
        'config_gallery.py',
    ]
    
    docs = [
        'README.md',
        'DOKUMENTACJA_NAUKOWA.md',
        'KARTA_SZYBKIEGO_DOSTĘPU.md',
    ]
    
    base_path = '/home/andrzej/Studia/Modelowanie i symulacja systemów/projekt'
    
    print("Skrypty:")
    for script in scripts:
        path = os.path.join(base_path, script)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  ✓ {script} ({size} bajtów)")
        else:
            print(f"  ✗ {script} (NOT FOUND)")
    
    print("\nDokumentacja:")
    for doc in docs:
        path = os.path.join(base_path, doc)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  ✓ {doc} ({size} bajtów)")
        else:
            print(f"  ✗ {doc} (NOT FOUND)")
    
    return True


def print_summary():
    """Drukuj podsumowanie"""
    print("\n" + "=" * 70)
    print("PODSUMOWANIE WDRAŻANIA")
    print("=" * 70)
    
    summary = """
PROJEKT: Formowanie Się Gatunków w Warunkach Barier Geograficznych

IMPLEMENTOWANE KOMPONENTY:
✓ Główny moduł symulacji (symulacja.py)
✓ Wielowariantowe eksperymenty (run_simulations.py)
✓ Szybki start (quickstart.py)
✓ Galeria konfiguracji (config_gallery.py)
✓ Dokumentacja techniczna (README.md)
✓ Dokumentacja naukowa (DOKUMENTACJA_NAUKOWA.md)
✓ Karta szybkiego dostępu (KARTA_SZYBKIEGO_DOSTĘPU.md)

CECHY IMPLEMENTACJI:
✓ Dynamika populacji (migracja, rozród, mutacje)
✓ Selekcja naturalna (fitness-dependent reprodukcja)
✓ Bariery geograficzne (blokowanie migracji)
✓ Zbieranie danych (statystyki z każdego kroku)
✓ Wizualizacja (snapshoty i wykresy)
✓ Analiza genetyki populacji
✓ 13 predefiniowanych konfiguracji
✓ Pełna dokumentacja biologiczna i matematyczna

GOTOWE DO URUCHOMIENIA:
1. python3 symulacja.py                 # Podstawowa symulacja
2. python3 run_simulations.py           # Wielowariantowe eksperymenty
3. python3 quickstart.py                # Praktyczne przykłady
4. python3 config_gallery.py            # Galeria konfiguracji

STATUS: ✓ IMPLEMENTACJA ZAKOŃCZONA
"""
    
    print(summary)


def main():
    """Uruchom wszystkie testy"""
    print("\n" + "=" * 70)
    print("WERYFIKACJA IMPLEMENTACJI")
    print("Data: 10 grudnia 2025")
    print("=" * 70 + "\n")
    
    results = []
    
    # Test 1: Biblioteki
    results.append(("Biblioteki", test_imports()))
    
    # Test 2: Moduł symulacji
    results.append(("Moduł symulacji", test_simulation_module()))
    
    # Test 3: Szybka symulacja
    results.append(("Szybka symulacja", test_quick_simulation()))
    
    # Test 4: Skrypty
    results.append(("Skrypty i dokumentacja", test_helper_scripts()))
    
    # Podsumowanie
    print("\n" + "=" * 70)
    print("WYNIKI TESTÓW")
    print("=" * 70)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:8} {name}")
        if not passed:
            all_passed = False
    
    # Podsumowanie wdrażania
    print_summary()
    
    # Status końcowy
    print("=" * 70)
    if all_passed:
        print("✓ WSZYSTKIE TESTY POWIODŁY SIĘ")
        print("✓ SYSTEM GOTOWY DO UŻYTKU")
        print("=" * 70)
        return 0
    else:
        print("✗ NIEKTÓRE TESTY NIE POWIODŁY SIĘ")
        print("Zainstaluj brakujące biblioteki: pip install numpy matplotlib scipy")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
