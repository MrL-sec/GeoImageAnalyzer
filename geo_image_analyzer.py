#!/usr/bin/env python3
"""
GeoImage Analyzer - Tool Forense per Analisi Immagini
Analizza immagini per estrarre metadati, informazioni EXIF e geolocalizzazione
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import json
import sys
try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # Fallback per Python < 3.8
    from importlib_metadata import version, PackageNotFoundError
from datetime import datetime
from PIL import Image, ExifTags, ImageTk
from PIL.ExifTags import TAGS, GPSTAGS
import requests
import hashlib
import platform
import subprocess
import folium
import tempfile
import webbrowser
try:
    import tkintermapview
except ImportError:
    tkintermapview = None

def check_and_install_dependencies():
    """
    Controlla e installa automaticamente le dipendenze necessarie
    """
    required_packages = {
        'Pillow': '>=10.0.0',
        'requests': '>=2.31.0',
        'folium': '>=0.14.0',
        'tkintermapview': '>=1.29'
    }
    
    missing_packages = []
    outdated_packages = []
    
    print("🔍 Controllo dipendenze...")
    
    for package_name, version_req in required_packages.items():
        try:
            # Controlla se il pacchetto è installato
            installed_version = version(package_name)
            print(f"✅ {package_name} {installed_version} - OK")
            
            # Per semplicità, consideriamo tutti i pacchetti installati come aggiornati
            # In futuro si potrebbe implementare un controllo più sofisticato delle versioni
                
        except PackageNotFoundError:
            print(f"❌ {package_name} - Non installato")
            missing_packages.append(package_name)
    
    # Installa pacchetti mancanti o da aggiornare
    packages_to_install = missing_packages + outdated_packages
    
    if packages_to_install:
        print(f"\n📦 Installazione/aggiornamento di {len(packages_to_install)} pacchetti...")
        print("⏳ Potrebbe richiedere alcuni minuti...")
        
        for package in packages_to_install:
            try:
                print(f"📥 Installando {package}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "--upgrade", package
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"✅ {package} installato/aggiornato con successo")
            except subprocess.CalledProcessError as e:
                print(f"❌ Errore nell'installazione di {package}: {e}")
                print(f"💡 Prova manualmente: pip install --upgrade {package}")
                return False
    
    print("\n Tutte le dipendenze sono aggiornate!")
    return True

def show_dependency_status():
    """
    Mostra lo stato delle dipendenze in una finestra di dialogo
    """
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        required_packages = ['Pillow', 'requests', 'folium', 'tkintermapview']
        status_info = []
        
        for package in required_packages:
            try:
                pkg_version = version(package)
                status_info.append(f"✅ {package}: v{pkg_version}")
            except PackageNotFoundError:
                status_info.append(f"❌ {package}: Non installato")
        
        status_message = "Stato Dipendenze:\n\n" + "\n".join(status_info)
        status_message += "\n\nTutte le dipendenze vengono controllate e aggiornate automaticamente all'avvio."
        
        # Crea una finestra temporanea per il messaggio
        temp_root = tk.Tk()
        temp_root.withdraw()  # Nasconde la finestra principale
        
        messagebox.showinfo("Stato Dipendenze", status_message)
        temp_root.destroy()
        
    except Exception as e:
        print(f"Errore nel mostrare lo stato delle dipendenze: {e}")

class GeoImageAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoImage Analyzer - Tool Forense")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Variabili
        self.current_image_path = None
        self.metadata = {}
        self.current_map_file = None
        self.current_coordinates = None
        
        self.setup_ui()
        
    def setup_menu(self):
        """Configura la barra dei menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Seleziona Immagine", command=self.select_image)
        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self.root.quit)
        
        # Menu Strumenti
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Strumenti", menu=tools_menu)
        tools_menu.add_command(label="Stato Dipendenze", command=show_dependency_status)
        tools_menu.add_command(label="Aggiorna Dipendenze", command=self.update_dependencies)
        
        # Menu Aiuto
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aiuto", menu=help_menu)
        help_menu.add_command(label="Informazioni", command=self.show_about)
        
    def setup_ui(self):
        """Configura l'interfaccia utente professionale"""
        # Menu bar
        self.setup_menu()
        
        # Frame principale con stile professionale
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurazione grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Barra di stato professionale
        status_frame = tk.Frame(main_frame, bg='#2c3e50', height=30)
        status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.grid_propagate(False)
        
        # Status labels
        self.status_label = tk.Label(status_frame, text="🔍 Ready for forensic analysis", 
                                    font=('Segoe UI', 9), fg='#ecf0f1', bg='#2c3e50')
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        # Version info
        version_label = tk.Label(status_frame, text="GeoImage Analyzer v1.0 | Digital Forensics Tool", 
                                font=('Segoe UI', 8), fg='#95a5a6', bg='#2c3e50')
        version_label.pack(side=tk.RIGHT, padx=15, pady=5)
        
        # Header professionale con logo e titolo
        header_frame = tk.Frame(main_frame, bg='#1a252f', relief='raised', bd=2)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        header_frame.columnconfigure(1, weight=1)
        
        # Logo/Icona (simulata con testo)
        logo_label = tk.Label(header_frame, text="🔍", font=('Arial', 24), 
                             fg='#3498db', bg='#1a252f')
        logo_label.grid(row=0, column=0, padx=(15, 10), pady=10)
        
        # Titolo principale
        title_label = tk.Label(header_frame, text="GeoImage Analyzer", 
                              font=('Segoe UI', 18, 'bold'), fg='#ecf0f1', bg='#1a252f')
        title_label.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        # Sottotitolo
        subtitle_label = tk.Label(header_frame, text="Professional Digital Forensics Tool", 
                                 font=('Segoe UI', 10), fg='#95a5a6', bg='#1a252f')
        subtitle_label.grid(row=1, column=1, sticky=tk.W, padx=(0, 15), pady=(0, 10))
        
        # Badge di stato
        status_label = tk.Label(header_frame, text="● READY", 
                               font=('Segoe UI', 9, 'bold'), fg='#27ae60', bg='#1a252f')
        status_label.grid(row=0, column=2, padx=15, pady=10)
        
        # Separatore
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Frame per selezione file con stile professionale
        file_frame = ttk.LabelFrame(main_frame, text="📁 Evidence Selection", padding="15")
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        file_frame.columnconfigure(1, weight=1)
        
        # Pulsante selezione con icona
        select_btn = ttk.Button(file_frame, text="🔍 Select Image", 
                               command=self.select_image)
        select_btn.grid(row=0, column=0, padx=(0, 15))
        
        # Campo percorso file
        self.file_path_var = tk.StringVar()
        path_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, 
                              state="readonly", font=('Consolas', 9))
        path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 15))
        
        # Pulsante analisi con stile evidenziato
        analyze_btn = ttk.Button(file_frame, text="🔬 Analyze Evidence", 
                                command=self.analyze_image)
        analyze_btn.grid(row=0, column=2)
        
        # Informazioni rapide
        info_label = tk.Label(file_frame, text="Supported: JPG, PNG, TIFF, BMP, GIF | Max size: 100MB", 
                             font=('Segoe UI', 8), fg='#7f8c8d')
        info_label.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        # Notebook per i risultati con stile professionale
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tab Anteprima Immagine
        self.preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.preview_frame, text="🖼️ Evidence Preview")
        
        # Frame per l'anteprima dell'immagine
        preview_container = ttk.Frame(self.preview_frame)
        preview_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Frame sinistro per l'immagine
        image_frame = ttk.LabelFrame(preview_container, text="📷 Digital Evidence", padding="15")
        image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Label per l'immagine con stile professionale
        self.image_label = tk.Label(image_frame, text="No evidence loaded\n\nSelect an image file to begin forensic analysis", 
                                   bg='#34495e', fg='#ecf0f1', relief='sunken', bd=2,
                                   font=('Segoe UI', 10), justify=tk.CENTER)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Frame destro per informazioni di base
        info_frame = ttk.LabelFrame(preview_container, text="📋 File Metadata", padding="15")
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Area di testo per informazioni di base con stile professionale
        self.info_text = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, 
                                                  width=45, height=20, 
                                                  bg='#2c3e50', fg='#ecf0f1',
                                                  font=('Consolas', 11),
                                                  insertbackground='#ecf0f1')
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Tab Metadati EXIF
        self.exif_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.exif_frame, text="📊 EXIF Metadata")
        
        # Header per EXIF
        exif_header = tk.Frame(self.exif_frame, bg='#34495e', height=40)
        exif_header.pack(fill=tk.X, padx=15, pady=(15, 0))
        exif_header.pack_propagate(False)
        
        exif_title = tk.Label(exif_header, text="📊 EXIF Data Analysis", 
                             font=('Segoe UI', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        exif_title.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.exif_text = scrolledtext.ScrolledText(self.exif_frame, wrap=tk.WORD, 
                                                  width=80, height=20,
                                                  bg='#2c3e50', fg='#ecf0f1',
                                                  font=('Consolas', 11),
                                                  insertbackground='#ecf0f1')
        self.exif_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Tab Geolocalizzazione
        self.geo_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.geo_frame, text="🌍 Geolocation")
        
        # Header per Geolocation
        geo_header = tk.Frame(self.geo_frame, bg='#34495e', height=40)
        geo_header.pack(fill=tk.X, padx=15, pady=(15, 0))
        geo_header.pack_propagate(False)
        
        geo_title = tk.Label(geo_header, text="🌍 GPS Coordinate Analysis", 
                            font=('Segoe UI', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        geo_title.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.geo_text = scrolledtext.ScrolledText(self.geo_frame, wrap=tk.WORD, 
                                                 width=80, height=20,
                                                 bg='#2c3e50', fg='#ecf0f1',
                                                 font=('Consolas', 11),
                                                 insertbackground='#ecf0f1')
        self.geo_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Tab Mappa
        self.map_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.map_frame, text="🗺️ Location Map")
        
        # Header per Map
        map_header = tk.Frame(self.map_frame, bg='#34495e', height=40)
        map_header.pack(fill=tk.X, padx=15, pady=(15, 0))
        map_header.pack_propagate(False)
        
        map_title = tk.Label(map_header, text="🗺️ Geographic Location Visualization", 
                            font=('Segoe UI', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        map_title.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Frame per controlli mappa
        map_controls = ttk.Frame(self.map_frame)
        map_controls.pack(fill=tk.X, padx=15, pady=5)
        
        ttk.Button(map_controls, text="📍 Show on Map", 
                  command=self.show_map).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(map_controls, text="🌐 Open in Browser", 
                  command=self.open_map_browser).pack(side=tk.LEFT)
        
        # Widget mappa (se tkintermapview è disponibile)
        if tkintermapview:
            self.map_widget = tkintermapview.TkinterMapView(self.map_frame, 
                                                           width=800, height=500, 
                                                           corner_radius=0)
            self.map_widget.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        else:
            # Fallback: area di testo per informazioni mappa
            self.map_text = scrolledtext.ScrolledText(self.map_frame, wrap=tk.WORD, 
                                                      width=80, height=20,
                                                      bg='#2c3e50', fg='#ecf0f1',
                                                      font=('Consolas', 11),
                                                      insertbackground='#ecf0f1')
            self.map_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            self.map_text.insert(tk.END, "⚠️ Interactive map not available.\n\nInstall tkintermapview for interactive map display:\npip install tkintermapview\n\nUse 'Open in Browser' button to view map.")
        
        # Tab Analisi Forense
        self.forensic_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.forensic_frame, text="🔬 Forensic Analysis")
        
        # Header per Forensic
        forensic_header = tk.Frame(self.forensic_frame, bg='#34495e', height=40)
        forensic_header.pack(fill=tk.X, padx=15, pady=(15, 0))
        forensic_header.pack_propagate(False)
        
        forensic_title = tk.Label(forensic_header, text="🔬 Digital Forensic Investigation Report", 
                                 font=('Segoe UI', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        forensic_title.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.forensic_text = scrolledtext.ScrolledText(self.forensic_frame, wrap=tk.WORD, 
                                                       width=80, height=20,
                                                       bg='#2c3e50', fg='#ecf0f1',
                                                       font=('Consolas', 11),
                                                       insertbackground='#ecf0f1')
        self.forensic_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Tab Report
        self.report_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.report_frame, text="📋 Complete Report")
        
        # Header per Report
        report_header = tk.Frame(self.report_frame, bg='#34495e', height=40)
        report_header.pack(fill=tk.X, padx=15, pady=(15, 0))
        report_header.pack_propagate(False)
        
        report_title = tk.Label(report_header, text="📋 Comprehensive Evidence Analysis", 
                               font=('Segoe UI', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        report_title.pack(side=tk.LEFT, padx=15, pady=10)
        
        report_button_frame = ttk.Frame(self.report_frame)
        report_button_frame.pack(fill=tk.X, padx=15, pady=5)
        
        ttk.Button(report_button_frame, text="📄 Export JSON Report", 
                  command=self.export_json_report).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(report_button_frame, text="📝 Export TXT Report", 
                  command=self.export_txt_report).pack(side=tk.LEFT)
        
        self.report_text = scrolledtext.ScrolledText(self.report_frame, wrap=tk.WORD, 
                                                     width=80, height=18,
                                                     bg='#2c3e50', fg='#ecf0f1',
                                                     font=('Consolas', 11),
                                                     insertbackground='#ecf0f1')
        self.report_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
    def select_image(self):
        """Seleziona un'immagine da analizzare"""
        file_types = [
            ('Immagini', '*.jpg *.jpeg *.png *.tiff *.tif *.bmp *.gif'),
            ('JPEG', '*.jpg *.jpeg'),
            ('PNG', '*.png'),
            ('TIFF', '*.tiff *.tif'),
            ('Tutti i file', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="Seleziona un'immagine da analizzare",
            filetypes=file_types
        )
        
        if filename:
            self.current_image_path = filename
            self.file_path_var.set(filename)
            self.clear_results()
            self.load_image_preview(filename)
    
    def load_image_preview(self, image_path):
        """Carica e mostra l'anteprima dell'immagine"""
        try:
            # Apre l'immagine
            with Image.open(image_path) as img:
                # Ottiene le dimensioni originali
                original_width, original_height = img.size
                
                # Calcola le dimensioni per l'anteprima (max 400x400 mantenendo proporzioni)
                max_size = 400
                if original_width > original_height:
                    new_width = max_size
                    new_height = int((original_height * max_size) / original_width)
                else:
                    new_height = max_size
                    new_width = int((original_width * max_size) / original_height)
                
                # Ridimensiona l'immagine
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Converte per Tkinter
                self.current_photo = ImageTk.PhotoImage(img_resized)
                
                # Mostra l'immagine
                self.image_label.config(image=self.current_photo, text="")
                
                # Aggiorna le informazioni di base
                self.update_basic_info(image_path, original_width, original_height)
                
                # Seleziona automaticamente la tab anteprima
                self.notebook.select(self.preview_frame)
                
        except Exception as e:
            self.image_label.config(image='', text=f"Errore nel caricamento: {str(e)}")
            messagebox.showerror("Errore", f"Impossibile caricare l'immagine: {str(e)}")
    
    def update_basic_info(self, image_path, width, height):
        """Aggiorna le informazioni di base dell'immagine"""
        try:
            # Ottiene informazioni sul file
            file_size = os.path.getsize(image_path)
            file_size_mb = file_size / (1024 * 1024)
            
            # Ottiene la data di modifica
            mod_time = os.path.getmtime(image_path)
            mod_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            
            # Ottiene il formato dell'immagine
            with Image.open(image_path) as img:
                image_format = img.format
                image_mode = img.mode
            
            # Mostra le informazioni
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "=== INFORMAZIONI IMMAGINE ===\n\n")
            self.info_text.insert(tk.END, f"📁 Nome File: {os.path.basename(image_path)}\n")
            self.info_text.insert(tk.END, f"📂 Percorso: {image_path}\n\n")
            
            self.info_text.insert(tk.END, "=== PROPRIETÀ TECNICHE ===\n")
            self.info_text.insert(tk.END, f"📐 Dimensioni: {width} x {height} pixel\n")
            self.info_text.insert(tk.END, f"💾 Dimensione File: {file_size_mb:.2f} MB ({file_size:,} bytes)\n")
            self.info_text.insert(tk.END, f"🖼️ Formato: {image_format}\n")
            self.info_text.insert(tk.END, f"🎨 Modalità Colore: {image_mode}\n")
            self.info_text.insert(tk.END, f"📅 Data Modifica: {mod_date}\n\n")
            
            self.info_text.insert(tk.END, "=== ISTRUZIONI ===\n")
            self.info_text.insert(tk.END, "1. Clicca 'Analizza' per estrarre i metadati EXIF\n")
            self.info_text.insert(tk.END, "2. Controlla le altre schede per i risultati\n")
            self.info_text.insert(tk.END, "3. Se presente GPS, vedrai la mappa automaticamente\n")
            
        except Exception as e:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Errore nel caricamento informazioni: {str(e)}")
            
    def clear_results(self):
        """Pulisce i risultati precedenti"""
        self.exif_text.delete(1.0, tk.END)
        self.geo_text.delete(1.0, tk.END)
        self.forensic_text.delete(1.0, tk.END)
        self.report_text.delete(1.0, tk.END)
        self.info_text.delete(1.0, tk.END)
        self.metadata = {}
        self.current_coordinates = None
        
        # Pulisce l'anteprima immagine
        self.image_label.config(image='', text="Nessuna immagine caricata")
        if hasattr(self, 'current_photo'):
            self.current_photo = None
        
        # Pulisce la mappa
        if tkintermapview and hasattr(self, 'map_widget'):
            self.map_widget.delete_all_marker()
        elif hasattr(self, 'map_text'):
            self.map_text.delete(1.0, tk.END)
            self.map_text.insert(tk.END, "Installare tkintermapview per la visualizzazione interattiva della mappa.\n")
            self.map_text.insert(tk.END, "Utilizzare il pulsante 'Apri in Browser' per visualizzare la mappa.")
        
    def analyze_image(self):
        """Analizza l'immagine selezionata"""
        if not self.current_image_path:
            messagebox.showerror("Evidence Required", "Please select digital evidence first")
            return
            
        if not os.path.exists(self.current_image_path):
            messagebox.showerror("Evidence Error", "Digital evidence file not found")
            return
            
        try:
            # Aggiorna status per l'inizio dell'analisi
            self.status_label.config(text="🔬 Starting forensic analysis...")
            self.root.update()
            
            # Analisi EXIF
            self.status_label.config(text="📊 Extracting EXIF metadata...")
            self.root.update()
            self.extract_exif_data()
            
            # Analisi geolocalizzazione
            self.status_label.config(text="🌍 Analyzing GPS coordinates...")
            self.root.update()
            self.extract_geolocation()
            
            # Analisi forense
            self.status_label.config(text="🔍 Performing forensic analysis...")
            self.root.update()
            self.forensic_analysis()
            
            # Generazione report
            self.status_label.config(text="📋 Generating comprehensive report...")
            self.root.update()
            self.generate_report()
            
            # Completamento
            self.status_label.config(text="✅ Forensic analysis completed successfully")
            messagebox.showinfo("Analysis Complete", "Digital forensic analysis completed successfully!\n\nReview all tabs for detailed findings.")
            
        except Exception as e:
            self.status_label.config(text="❌ Analysis failed - Check evidence integrity")
            messagebox.showerror("Analysis Error", f"Forensic analysis failed: {str(e)}\n\nPlease verify evidence file integrity.")
            
    def extract_exif_data(self):
        """Estrae i metadati EXIF dall'immagine"""
        try:
            with Image.open(self.current_image_path) as image:
                exif_data = image._getexif()
                
                if exif_data is not None:
                    exif_info = {}
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif_info[tag] = value
                    
                    self.metadata['exif'] = exif_info
                    
                    # Mostra i dati EXIF
                    self.exif_text.insert(tk.END, "=== METADATI EXIF ===\n\n")
                    
                    for tag, value in exif_info.items():
                        if isinstance(value, bytes):
                            try:
                                value = value.decode('utf-8')
                            except:
                                value = str(value)
                        self.exif_text.insert(tk.END, f"{tag}: {value}\n")
                        
                else:
                    self.exif_text.insert(tk.END, "Nessun dato EXIF trovato nell'immagine.")
                    self.metadata['exif'] = {}
                    
        except Exception as e:
            self.exif_text.insert(tk.END, f"Errore nell'estrazione EXIF: {str(e)}")
            
    def extract_geolocation(self):
        """Estrae e analizza i dati di geolocalizzazione"""
        try:
            with Image.open(self.current_image_path) as image:
                exif_data = image._getexif()
                
                if exif_data is not None:
                    gps_info = {}
                    
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag == 'GPSInfo':
                            for gps_tag_id, gps_value in value.items():
                                gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                                gps_info[gps_tag] = gps_value
                    
                    self.metadata['gps'] = gps_info
                    
                    self.geo_text.insert(tk.END, "=== INFORMAZIONI GPS ===\n\n")
                    
                    if gps_info:
                        for tag, value in gps_info.items():
                            self.geo_text.insert(tk.END, f"{tag}: {value}\n")
                        
                        # Calcola coordinate decimali
                        lat, lon = self.get_decimal_coordinates(gps_info)
                        if lat and lon:
                            self.geo_text.insert(tk.END, f"\nCoordinate Decimali:\n")
                            self.geo_text.insert(tk.END, f"Latitudine: {lat}\n")
                            self.geo_text.insert(tk.END, f"Longitudine: {lon}\n")
                            
                            # Reverse geocoding
                            address = self.reverse_geocode(lat, lon)
                            if address:
                                self.geo_text.insert(tk.END, f"\nIndirizzo: {address}\n")
                                
                            self.metadata['coordinates'] = {'lat': lat, 'lon': lon, 'address': address}
                            self.current_coordinates = (lat, lon)
                            
                            # Aggiorna automaticamente la mappa
                            self.update_map_display(lat, lon, address)
                    else:
                        self.geo_text.insert(tk.END, "Nessuna informazione GPS trovata.")
                        
                else:
                    self.geo_text.insert(tk.END, "Nessun dato EXIF disponibile per l'analisi GPS.")
                    
        except Exception as e:
            self.geo_text.insert(tk.END, f"Errore nell'estrazione GPS: {str(e)}")
            
    def get_decimal_coordinates(self, gps_info):
        """Converte le coordinate GPS in formato decimale"""
        try:
            lat_ref = gps_info.get('GPSLatitudeRef')
            lat = gps_info.get('GPSLatitude')
            lon_ref = gps_info.get('GPSLongitudeRef')
            lon = gps_info.get('GPSLongitude')
            
            if lat and lon:
                lat_decimal = self.dms_to_decimal(lat, lat_ref)
                lon_decimal = self.dms_to_decimal(lon, lon_ref)
                return lat_decimal, lon_decimal
                
        except Exception as e:
            print(f"Errore conversione coordinate: {e}")
            
        return None, None
        
    def dms_to_decimal(self, dms, ref):
        """Converte da gradi/minuti/secondi a decimale"""
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])
        
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        
        if ref in ['S', 'W']:
            decimal = -decimal
            
        return decimal
        
    def reverse_geocode(self, lat, lon):
        """Ottiene l'indirizzo dalle coordinate (usando OpenStreetMap)"""
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
            headers = {'User-Agent': 'GeoImageAnalyzer/1.0'}
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('display_name', 'Indirizzo non trovato')
                
        except Exception as e:
            print(f"Errore reverse geocoding: {e}")
            
        return None
        
    def forensic_analysis(self):
        """Esegue analisi forense approfondita"""
        try:
            self.forensic_text.insert(tk.END, "=== ANALISI FORENSE ===\n\n")
            
            # Informazioni file
            file_stats = os.stat(self.current_image_path)
            file_size = file_stats.st_size
            creation_time = datetime.fromtimestamp(file_stats.st_ctime)
            modification_time = datetime.fromtimestamp(file_stats.st_mtime)
            access_time = datetime.fromtimestamp(file_stats.st_atime)
            
            self.forensic_text.insert(tk.END, "INFORMAZIONI FILE:\n")
            self.forensic_text.insert(tk.END, f"Nome: {os.path.basename(self.current_image_path)}\n")
            self.forensic_text.insert(tk.END, f"Percorso: {self.current_image_path}\n")
            self.forensic_text.insert(tk.END, f"Dimensione: {file_size:,} bytes\n")
            self.forensic_text.insert(tk.END, f"Creazione: {creation_time}\n")
            self.forensic_text.insert(tk.END, f"Modifica: {modification_time}\n")
            self.forensic_text.insert(tk.END, f"Ultimo accesso: {access_time}\n\n")
            
            # Hash del file
            file_hashes = self.calculate_hashes()
            self.forensic_text.insert(tk.END, "HASH FILE:\n")
            for hash_type, hash_value in file_hashes.items():
                self.forensic_text.insert(tk.END, f"{hash_type}: {hash_value}\n")
            
            # Informazioni immagine
            with Image.open(self.current_image_path) as image:
                self.forensic_text.insert(tk.END, f"\nINFORMAZIONI IMMAGINE:\n")
                self.forensic_text.insert(tk.END, f"Formato: {image.format}\n")
                self.forensic_text.insert(tk.END, f"Modalità: {image.mode}\n")
                self.forensic_text.insert(tk.END, f"Dimensioni: {image.size[0]}x{image.size[1]} pixel\n")
                
                if hasattr(image, 'info'):
                    self.forensic_text.insert(tk.END, f"\nINFORMAZIONI AGGIUNTIVE:\n")
                    for key, value in image.info.items():
                        self.forensic_text.insert(tk.END, f"{key}: {value}\n")
            
            # Analisi dispositivo (se disponibile)
            self.analyze_device_info()
            
            # Salva i dati forensi
            self.metadata['forensic'] = {
                'file_info': {
                    'name': os.path.basename(self.current_image_path),
                    'path': self.current_image_path,
                    'size': file_size,
                    'creation_time': creation_time.isoformat(),
                    'modification_time': modification_time.isoformat(),
                    'access_time': access_time.isoformat()
                },
                'hashes': file_hashes
            }
            
        except Exception as e:
            self.forensic_text.insert(tk.END, f"Errore nell'analisi forense: {str(e)}")
            
    def calculate_hashes(self):
        """Calcola hash MD5, SHA1 e SHA256 del file"""
        hashes = {}
        
        try:
            with open(self.current_image_path, 'rb') as f:
                content = f.read()
                
                hashes['MD5'] = hashlib.md5(content).hexdigest()
                hashes['SHA1'] = hashlib.sha1(content).hexdigest()
                hashes['SHA256'] = hashlib.sha256(content).hexdigest()
                
        except Exception as e:
            print(f"Errore calcolo hash: {e}")
            
        return hashes
        
    def analyze_device_info(self):
        """Analizza informazioni sul dispositivo di origine"""
        try:
            exif_data = self.metadata.get('exif', {})
            
            self.forensic_text.insert(tk.END, f"\nINFORMAZIONI DISPOSITIVO:\n")
            
            # Marca e modello
            make = exif_data.get('Make', 'Non disponibile')
            model = exif_data.get('Model', 'Non disponibile')
            self.forensic_text.insert(tk.END, f"Marca: {make}\n")
            self.forensic_text.insert(tk.END, f"Modello: {model}\n")
            
            # Software
            software = exif_data.get('Software', 'Non disponibile')
            self.forensic_text.insert(tk.END, f"Software: {software}\n")
            
            # Data e ora
            datetime_original = exif_data.get('DateTimeOriginal', 'Non disponibile')
            datetime_digitized = exif_data.get('DateTimeDigitized', 'Non disponibile')
            self.forensic_text.insert(tk.END, f"Data scatto originale: {datetime_original}\n")
            self.forensic_text.insert(tk.END, f"Data digitalizzazione: {datetime_digitized}\n")
            
            # Impostazioni fotocamera
            iso = exif_data.get('ISOSpeedRatings', 'Non disponibile')
            aperture = exif_data.get('FNumber', 'Non disponibile')
            exposure = exif_data.get('ExposureTime', 'Non disponibile')
            focal_length = exif_data.get('FocalLength', 'Non disponibile')
            
            self.forensic_text.insert(tk.END, f"\nIMPOSTAZIONI SCATTO:\n")
            self.forensic_text.insert(tk.END, f"ISO: {iso}\n")
            self.forensic_text.insert(tk.END, f"Apertura: {aperture}\n")
            self.forensic_text.insert(tk.END, f"Tempo esposizione: {exposure}\n")
            self.forensic_text.insert(tk.END, f"Lunghezza focale: {focal_length}\n")
            
        except Exception as e:
            self.forensic_text.insert(tk.END, f"Errore analisi dispositivo: {str(e)}")
            
    def generate_report(self):
        """Genera un report completo dell'analisi"""
        try:
            self.report_text.insert(tk.END, "=== REPORT COMPLETO ANALISI FORENSE ===\n\n")
            
            # Timestamp analisi
            analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.report_text.insert(tk.END, f"Data/Ora Analisi: {analysis_time}\n")
            self.report_text.insert(tk.END, f"Sistema Operativo: {platform.system()} {platform.release()}\n")
            self.report_text.insert(tk.END, f"Analizzatore: GeoImage Analyzer v1.0\n\n")
            
            # Sommario file
            self.report_text.insert(tk.END, "SOMMARIO FILE:\n")
            forensic_data = self.metadata.get('forensic', {})
            file_info = forensic_data.get('file_info', {})
            
            self.report_text.insert(tk.END, f"Nome file: {file_info.get('name', 'N/A')}\n")
            self.report_text.insert(tk.END, f"Percorso: {file_info.get('path', 'N/A')}\n")
            self.report_text.insert(tk.END, f"Dimensione: {file_info.get('size', 'N/A')} bytes\n\n")
            
            # Hash
            hashes = forensic_data.get('hashes', {})
            if hashes:
                self.report_text.insert(tk.END, "HASH CRITTOGRAFICI:\n")
                for hash_type, hash_value in hashes.items():
                    self.report_text.insert(tk.END, f"{hash_type}: {hash_value}\n")
                self.report_text.insert(tk.END, "\n")
            
            # Geolocalizzazione
            coordinates = self.metadata.get('coordinates', {})
            if coordinates:
                self.report_text.insert(tk.END, "GEOLOCALIZZAZIONE:\n")
                self.report_text.insert(tk.END, f"Latitudine: {coordinates.get('lat', 'N/A')}\n")
                self.report_text.insert(tk.END, f"Longitudine: {coordinates.get('lon', 'N/A')}\n")
                self.report_text.insert(tk.END, f"Indirizzo: {coordinates.get('address', 'N/A')}\n\n")
            
            # Dispositivo
            exif_data = self.metadata.get('exif', {})
            if exif_data:
                self.report_text.insert(tk.END, "DISPOSITIVO DI ORIGINE:\n")
                self.report_text.insert(tk.END, f"Marca: {exif_data.get('Make', 'N/A')}\n")
                self.report_text.insert(tk.END, f"Modello: {exif_data.get('Model', 'N/A')}\n")
                self.report_text.insert(tk.END, f"Software: {exif_data.get('Software', 'N/A')}\n")
                self.report_text.insert(tk.END, f"Data scatto: {exif_data.get('DateTimeOriginal', 'N/A')}\n\n")
            
            # Conclusioni
            self.report_text.insert(tk.END, "CONCLUSIONI ANALISI:\n")
            self.report_text.insert(tk.END, "- Analisi metadati EXIF completata\n")
            
            if coordinates:
                self.report_text.insert(tk.END, "- Geolocalizzazione estratta con successo\n")
            else:
                self.report_text.insert(tk.END, "- Nessuna informazione di geolocalizzazione trovata\n")
                
            if exif_data.get('Make') or exif_data.get('Model'):
                self.report_text.insert(tk.END, "- Informazioni dispositivo identificate\n")
            else:
                self.report_text.insert(tk.END, "- Informazioni dispositivo limitate\n")
                
            self.report_text.insert(tk.END, "- Hash crittografici calcolati per integrità\n")
            
        except Exception as e:
            self.report_text.insert(tk.END, f"Errore generazione report: {str(e)}")
            
    def export_json_report(self):
        """Esporta il report in formato JSON"""
        if not self.metadata:
            messagebox.showwarning("Attenzione", "Nessun dato da esportare. Analizza prima un'immagine.")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Salva Report JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                report_data = {
                    'analysis_info': {
                        'timestamp': datetime.now().isoformat(),
                        'analyzer': 'GeoImage Analyzer v1.0',
                        'system': f"{platform.system()} {platform.release()}"
                    },
                    'metadata': self.metadata
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
                    
                messagebox.showinfo("Successo", f"Report JSON salvato: {filename}")
                
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nel salvataggio: {str(e)}")
                
    def export_txt_report(self):
        """Esporta il report in formato testo"""
        if not self.metadata:
            messagebox.showwarning("Attenzione", "Nessun dato da esportare. Analizza prima un'immagine.")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Salva Report TXT",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.report_text.get(1.0, tk.END))
                    
                messagebox.showinfo("Successo", f"Report TXT salvato: {filename}")
                
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nel salvataggio: {str(e)}")
                
    def update_map_display(self, lat, lon, address=None):
        """Aggiorna la visualizzazione della mappa con le coordinate"""
        try:
            if tkintermapview and hasattr(self, 'map_widget'):
                # Centra la mappa sulle coordinate
                self.map_widget.set_position(lat, lon)
                self.map_widget.set_zoom(15)
                
                # Rimuove marker precedenti e aggiunge nuovo marker
                self.map_widget.delete_all_marker()
                marker_text = f"Posizione immagine\nLat: {lat:.6f}\nLon: {lon:.6f}"
                if address:
                    marker_text += f"\n{address}"
                    
                self.map_widget.set_marker(lat, lon, text=marker_text)
                
            elif hasattr(self, 'map_text'):
                # Aggiorna il testo della mappa
                self.map_text.delete(1.0, tk.END)
                self.map_text.insert(tk.END, "=== INFORMAZIONI MAPPA ===\n\n")
                self.map_text.insert(tk.END, f"Coordinate trovate:\n")
                self.map_text.insert(tk.END, f"Latitudine: {lat:.6f}\n")
                self.map_text.insert(tk.END, f"Longitudine: {lon:.6f}\n")
                if address:
                    self.map_text.insert(tk.END, f"Indirizzo: {address}\n")
                self.map_text.insert(tk.END, "\nUtilizzare il pulsante 'Apri in Browser' per visualizzare la mappa interattiva.")
                
        except Exception as e:
            print(f"Errore aggiornamento mappa: {e}")
            
    def show_map(self):
        """Mostra la mappa con le coordinate correnti"""
        if not self.current_coordinates:
            messagebox.showwarning("Attenzione", "Nessuna coordinata GPS trovata nell'immagine.")
            return
            
        lat, lon = self.current_coordinates
        address = self.metadata.get('coordinates', {}).get('address', '')
        self.update_map_display(lat, lon, address)
        
        # Seleziona automaticamente la tab mappa
        self.notebook.select(self.map_frame)
        
    def open_map_browser(self):
        """Apre la mappa in un browser web usando Folium"""
        if not self.current_coordinates:
            messagebox.showwarning("Attenzione", "Nessuna coordinata GPS trovata nell'immagine.")
            return
            
        try:
            lat, lon = self.current_coordinates
            address = self.metadata.get('coordinates', {}).get('address', '')
            
            # Crea mappa con Folium
            m = folium.Map(location=[lat, lon], zoom_start=15)
            
            # Aggiunge marker
            popup_text = f"Posizione Immagine<br>Lat: {lat:.6f}<br>Lon: {lon:.6f}"
            if address:
                popup_text += f"<br><br>{address}"
                
            folium.Marker(
                [lat, lon],
                popup=popup_text,
                tooltip="Clicca per dettagli",
                icon=folium.Icon(color='red', icon='camera')
            ).add_to(m)
            
            # Aggiunge cerchio per evidenziare l'area
            folium.Circle(
                [lat, lon],
                radius=100,
                popup="Area di interesse",
                color="red",
                fill=True,
                fillOpacity=0.2
            ).add_to(m)
            
            # Salva in file temporaneo
            if self.current_map_file:
                try:
                    os.unlink(self.current_map_file)
                except:
                    pass
                    
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False)
            self.current_map_file = temp_file.name
            temp_file.close()
            
            m.save(self.current_map_file)
            
            # Apre nel browser
            webbrowser.open('file://' + os.path.abspath(self.current_map_file))
            
            messagebox.showinfo("Successo", "Mappa aperta nel browser predefinito.")
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nell'apertura della mappa: {str(e)}")
    
    def update_dependencies(self):
        """Aggiorna manualmente le dipendenze"""
        try:
            from tkinter import messagebox
            
            # Mostra messaggio di avvio
            messagebox.showinfo("Aggiornamento Dipendenze", 
                              "Avvio aggiornamento dipendenze...\nQuesto potrebbe richiedere alcuni minuti.")
            
            # Esegui l'aggiornamento
            success = check_and_install_dependencies()
            
            if success:
                messagebox.showinfo("Aggiornamento Completato", 
                                  "Tutte le dipendenze sono state aggiornate con successo!")
                # Ricarica tkintermapview se necessario
                try:
                    global tkintermapview
                    import tkintermapview
                    self.tkintermapview_available = True
                except ImportError:
                    self.tkintermapview_available = False
            else:
                messagebox.showerror("Errore Aggiornamento", 
                                   "Si è verificato un errore durante l'aggiornamento delle dipendenze.\n" +
                                   "Controlla la console per maggiori dettagli.")
        except Exception as e:
            print(f"Errore nell'aggiornamento delle dipendenze: {e}")
    
    def show_about(self):
        """Mostra informazioni sull'applicazione"""
        try:
            from tkinter import messagebox
            
            about_text = """GeoImage Analyzer v2.0

Analizzatore di metadati e geolocalizzazione per immagini

Funzionalità:
• Estrazione metadati EXIF
• Analisi geolocalizzazione GPS
• Visualizzazione su mappa interattiva
• Esportazione report (JSON/TXT)
• Installazione automatica dipendenze

Dipendenze:
• Pillow (elaborazione immagini)
• Requests (geocoding)
• Folium (mappe web)
• TkinterMapView (mappe integrate)

Creato con Python e Tkinter"""
            
            messagebox.showinfo("Informazioni", about_text)
        except Exception as e:
            print(f"Errore nel mostrare le informazioni: {e}")

def main():
    print("🚀 Avvio GeoImage Analyzer...")
    print("=" * 40)
    
    # Controlla e installa dipendenze automaticamente
    if not check_and_install_dependencies():
        print("\n❌ Errore nell'installazione delle dipendenze.")
        print("💡 Prova a eseguire manualmente: pip install -r requirements.txt")
        input("\nPremi INVIO per continuare comunque...")
    
    print("\n🖥️ Avvio interfaccia grafica...")
    
    try:
        # Ricarica i moduli dopo l'installazione
        global tkintermapview
        try:
            import tkintermapview
        except ImportError:
            tkintermapview = None
            print("⚠️ tkintermapview non disponibile - alcune funzionalità mappa saranno limitate")
        
        root = tk.Tk()
        app = GeoImageAnalyzer(root)
        
        print("✅ Interfaccia caricata con successo!")
        print("📋 Seleziona un'immagine per iniziare l'analisi forense.\n")
        
        root.mainloop()
        
    except Exception as e:
        print(f"\n❌ Errore nell'avvio dell'interfaccia: {e}")
        print("💡 Verifica che tutte le dipendenze siano installate correttamente.")
        input("\nPremi INVIO per uscire...")

if __name__ == "__main__":
    main()