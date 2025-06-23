#!/usr/bin/env python3
"""
GeoImage Analyzer - Script di Installazione
Installa automaticamente tutte le dipendenze necessarie
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def check_python_version():
    """Verifica la versione di Python"""
    print("Controllo versione Python...")
    
    if sys.version_info < (3, 7):
        print("❌ ERRORE: Python 3.7 o superiore è richiesto")
        print(f"Versione attuale: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - OK")
    return True

def check_pip():
    """Verifica che pip sia disponibile"""
    print("Controllo disponibilità pip...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip disponibile")
        return True
    except subprocess.CalledProcessError:
        print("❌ ERRORE: pip non trovato")
        print("Installa pip prima di continuare")
        return False

def install_requirements():
    """Installa le dipendenze dal file requirements.txt"""
    print("Installazione dipendenze...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ ERRORE: File requirements.txt non trovato")
        return False
    
    try:
        # Aggiorna pip
        print("Aggiornamento pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True)
        
        # Installa dipendenze
        print("Installazione pacchetti...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                      check=True)
        
        print("✅ Dipendenze installate con successo")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ ERRORE durante l'installazione: {e}")
        return False

def test_imports():
    """Testa l'importazione delle librerie principali"""
    print("Test importazione librerie...")
    
    required_modules = [
        ('PIL', 'Pillow'),
        ('requests', 'requests'),
        ('tkinter', 'tkinter (standard library)')
    ]
    
    all_ok = True
    
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
            print(f"✅ {package_name} - OK")
        except ImportError:
            print(f"❌ {package_name} - ERRORE")
            all_ok = False
    
    return all_ok

def create_desktop_shortcut():
    """Crea un collegamento sul desktop (solo per sistemi supportati)"""
    system = platform.system()
    script_dir = Path(__file__).parent
    main_script = script_dir / "geo_image_analyzer.py"
    
    if system == "Windows":
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "GeoImage Analyzer.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{main_script}"'
            shortcut.WorkingDirectory = str(script_dir)
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            print("✅ Collegamento desktop creato")
            
        except ImportError:
            print("⚠️  Impossibile creare collegamento desktop (winshell non disponibile)")
        except Exception as e:
            print(f"⚠️  Errore creazione collegamento: {e}")
            
    elif system == "Darwin":  # macOS
        try:
            app_script = f'''#!/bin/bash
cd "{script_dir}"
python3 "{main_script}"
'''
            
            app_path = os.path.expanduser("~/Desktop/GeoImage Analyzer.command")
            with open(app_path, 'w') as f:
                f.write(app_script)
            
            os.chmod(app_path, 0o755)
            print("✅ Script di avvio creato sul desktop")
            
        except Exception as e:
            print(f"⚠️  Errore creazione script: {e}")
            
    elif system == "Linux":
        try:
            desktop_entry = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=GeoImage Analyzer
Comment=Tool forense per analisi immagini
Exec=python3 "{main_script}"
Path={script_dir}
Icon=applications-graphics
Terminal=false
Categories=Graphics;Photography;Security;
'''
            
            desktop_path = os.path.expanduser("~/Desktop/GeoImage Analyzer.desktop")
            with open(desktop_path, 'w') as f:
                f.write(desktop_entry)
            
            os.chmod(desktop_path, 0o755)
            print("✅ File .desktop creato")
            
        except Exception as e:
            print(f"⚠️  Errore creazione file desktop: {e}")
    
    else:
        print(f"⚠️  Sistema {system} non supportato per collegamento automatico")

def create_run_script():
    """Crea script di avvio semplificato"""
    script_dir = Path(__file__).parent
    main_script = script_dir / "geo_image_analyzer.py"
    
    system = platform.system()
    
    if system == "Windows":
        run_script = script_dir / "run_analyzer.bat"
        content = f'''@echo off
cd /d "{script_dir}"
python "{main_script}"
pause
'''
    else:
        run_script = script_dir / "run_analyzer.sh"
        content = f'''#!/bin/bash
cd "{script_dir}"
python3 "{main_script}"
'''
    
    try:
        with open(run_script, 'w') as f:
            f.write(content)
        
        if system != "Windows":
            os.chmod(run_script, 0o755)
        
        print(f"✅ Script di avvio creato: {run_script.name}")
        
    except Exception as e:
        print(f"⚠️  Errore creazione script di avvio: {e}")

def main():
    """Funzione principale di installazione"""
    print("="*60)
    print("    GEOIMAGE ANALYZER - INSTALLAZIONE AUTOMATICA")
    print("="*60)
    print()
    
    # Informazioni sistema
    print(f"Sistema operativo: {platform.system()} {platform.release()}")
    print(f"Architettura: {platform.machine()}")
    print(f"Python: {sys.version}")
    print()
    
    # Controlli preliminari
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    # Installazione
    if not install_requirements():
        return False
    
    # Test
    if not test_imports():
        print("⚠️  Alcune librerie potrebbero non funzionare correttamente")
    
    # Script di avvio
    create_run_script()
    
    # Collegamento desktop (opzionale)
    response = input("\nCreare collegamento sul desktop? (s/n): ").lower().strip()
    if response in ['s', 'si', 'y', 'yes']:
        create_desktop_shortcut()
    
    print()
    print("="*60)
    print("✅ INSTALLAZIONE COMPLETATA CON SUCCESSO!")
    print("="*60)
    print()
    print("Per avviare GeoImage Analyzer:")
    print(f"  1. Esegui: python3 geo_image_analyzer.py")
    print(f"  2. Oppure usa lo script: ./run_analyzer.sh (Linux/Mac) o run_analyzer.bat (Windows)")
    print()
    print("Per testare le funzionalità:")
    print(f"  python3 example_usage.py")
    print()
    print("Documentazione completa disponibile in README.md")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInstallazione interrotta dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nErrore imprevisto durante l'installazione: {e}")
        sys.exit(1)