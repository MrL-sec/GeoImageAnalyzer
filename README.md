# GeoImage Analyzer - Tool Forense per Analisi Immagini

## Descrizione

GeoImage-Analyzer è un tool forense completo sviluppato in Python per l'analisi approfondita di immagini digitali. Il software è progettato per investigatori digitali, esperti di sicurezza informatica e professionisti forensi che necessitano di estrarre e analizzare metadati nascosti dalle immagini.

PER INSTALLARE LE DIPENDENZE AUTOMATICAMENTE ESEGUI " install.py "

## Funzionalità principali

### 🔍 Analisi Metadati EXIF
- Estrazione completa di tutti i metadati EXIF presenti nell'immagine
- Visualizzazione dettagliata di informazioni tecniche della fotocamera
- Identificazione del dispositivo di origine (marca, modello, software)
- Analisi delle impostazioni di scatto (ISO, apertura, tempo di esposizione)

### 🌍 Geolocalizzazione
- Estrazione delle coordinate GPS dalle immagini
- Conversione automatica da formato DMS a decimale
- Reverse geocoding per ottenere l'indirizzo fisico
- Mappatura della posizione geografica dove è stata scattata la foto

### 🖼️ Anteprima immagine
- **Visualizzazione immediata**: Anteprima dell'immagine caricata con ridimensionamento automatico
- **Informazioni di base**: Dimensioni, formato, dimensione file e data di modifica
- **Selezione automatica**: La tab anteprima si apre automaticamente al caricamento dell'immagine
- **Istruzioni integrate**: Guida passo-passo per l'utilizzo del tool
- **Gestione errori**: Messaggi informativi in caso di problemi nel caricamento

### 🗺️ Visualizzazione mappa
- **Mappa interattiva integrata** nell'interfaccia (tramite tkintermapview)
- **Visualizzazione automatica** delle coordinate GPS estratte
- **Apertura in browser** con mappa dettagliata (tramite Folium)
- **Cerchio di evidenziazione** dell'area di interesse
-

### 🔬 Analisi Forense
- Calcolo di hash crittografici (MD5, SHA1, SHA256) per verifica integrità
- Analisi dei timestamp del file (creazione, modifica, ultimo accesso)
- Informazioni dettagliate sul file (dimensione, formato, modalità colore)
- Identificazione di possibili modifiche o manipolazioni

### 📊 Reporting completo
- Generazione di report dettagliati in formato JSON e TXT
- Esportazione di tutti i dati per documentazione legale
- Interfaccia grafica intuitiva con visualizzazione a schede
- Cronologia completa dell'analisi

## Installazione

1. Clona il repository:
```bash
git clone https://github.com/MrL-sec/GeoImageAnalyzer.git
cd GeoImageAnalyzer
```

2. Avvia l'applicazione:
```bash
python geo_image_analyzer.py
```

**✨ Installazione automatica delle dipendenze**

Il tool ora installa automaticamente tutte le dipendenze necessarie al primo avvio! Non è più necessario eseguire manualmente `pip install -r requirements.txt`.

### Funzionalità di gestione dipendenze:
- **Controllo automatico**: Verifica la presenza di tutte le dipendenze all'avvio
- **Installazione automatica**: Installa automaticamente i pacchetti mancanti
- **Aggiornamento intelligente**: Rileva e aggiorna le dipendenze obsolete
- **Menu integrato**: Accesso alle funzioni di gestione dipendenze tramite menu "Strumenti"
- **Stato in tempo reale**: Visualizzazione dello stato delle dipendenze installate

### Installazione Manuale (Opzionale)
Se preferisci installare manualmente le dipendenze:
```bash
pip install -r requirements.txt
```

### Prerequisiti
- Python 3.7 o superiore
- Sistema operativo: Windows, macOS, Linux

### Dipendenze Principali
- **Pillow**: Elaborazione immagini e estrazione metadati EXIF
- **requests**: Comunicazione HTTP per servizi di geolocalizzazione
- **folium**: Generazione mappe interattive per browser
- **tkintermapview**: Widget mappa integrato nell'interfaccia
- **tkinter**: Interfaccia grafica (incluso in Python standard)

## 🚀 Utilizzo

### Interfaccia grafica
1. **Avvia l'applicazione**: `python geo_image_analyzer.py`
   Al primo avvio, il tool controllerà e installerà automaticamente tutte le dipendenze necessarie.

2. **Interfaccia e Menu**:
   - **Menu File**: Seleziona immagini e gestisci l'applicazione
   - **Menu Strumenti**: Controlla stato dipendenze e forza aggiornamenti
   - **Menu Aiuto**: Informazioni sull'applicazione e versione

3. Clicca "Seleziona Immagine" per scegliere il file da analizzare
4. Clicca "Analizza" per avviare l'analisi completa
5. Esplora i risultati nelle diverse schede:
   - **Anteprima Immagine**: Visualizzazione dell'immagine con informazioni di base
   - **Metadati EXIF**: Informazioni tecniche complete
   - **Geolocalizzazione**: Coordinate GPS e indirizzo
   - **🗺️ Mappa Localizzazione**: Visualizzazione interattiva della posizione
     - La mappa si aggiorna automaticamente quando vengono trovate coordinate GPS
     - Usa "Visualizza su Mappa" per centrare la vista
     - Usa "Apri in Browser" per una mappa dettagliata con Folium
   - **Analisi Forense**: Hash, timestamp e info dispositivo
   - **Report Completo**: Riepilogo di tutti i dati

6. **Gestione dipendenze**:
   - **Menu Strumenti > Stato Dipendenze**: Visualizza lo stato di tutte le librerie
   - **Menu Strumenti > Aggiorna Dipendenze**: Forza l'aggiornamento manuale

7. Esporta i risultati in formato JSON o TXT

### Procedura di analisi dettagliata

1. **Selezione immagine**
   - Clicca su "Seleziona Immagine"
   - Scegli il file immagine da analizzare
   - Formati supportati: JPEG, PNG, TIFF, BMP, GIF

2. **Avvio Analisi**
   - Clicca su "Analizza" per iniziare l'elaborazione
   - L'analisi viene eseguita automaticamente su tutti gli aspetti

3. **Visualizzazione risultati**
   - **Tab Metadati EXIF**: Tutti i metadati tecnici dell'immagine
   - **Tab Geolocalizzazione**: Coordinate GPS e indirizzo fisico
   - **Tab Analisi forense**: Hash, timestamp e informazioni file
   - **Tab Report Completo**: Riepilogo completo dell'analisi

4. **Esportazione**
   - Esporta i risultati in formato JSON per elaborazioni successive
   - Salva il report in formato TXT per documentazione

## Casi d'uso forensi

### Investigazioni digitali
- Verifica dell'autenticità di immagini in procedimenti legali
- Tracciamento della provenienza di contenuti digitali
- Identificazione di dispositivi utilizzati per acquisizioni

### Sicurezza informatica
- Analisi di immagini sospette in incidenti di sicurezza
- Verifica dell'integrità di prove digitali
- Identificazione di metadati sensibili in leak di dati

### Giornalismo investigativo
- Verifica della provenienza di immagini ricevute
- Identificazione di location e timestamp di eventi
- Controllo dell'autenticità di materiale fotografico

## Caratteristiche tecniche

### Formati supportati
- **JPEG/JPG**: Supporto completo per metadati EXIF e GPS
- **PNG**: Estrazione metadati disponibili
- **TIFF**: Analisi completa di metadati tecnici
- **BMP/GIF**: Informazioni base del file

### Sicurezza e privacy
- Tutte le analisi vengono eseguite localmente
- Nessun upload di immagini su server esterni
- Solo il reverse geocoding utilizza servizi online (OpenStreetMap)
- Possibilità di utilizzo completamente offline (escluso reverse geocoding)

### Accuratezza dei dati
- Estrazione diretta dai metadati EXIF originali
- Nessuna modifica o alterazione dei file analizzati
- Calcolo preciso di hash crittografici per verifica integrità
- Conversione accurata di coordinate GPS

## File di test

### 📁 test_image_with_gps.jpg

Il repository include un'immagine di test appositamente creata per dimostrare le funzionalità del GeoImage Analyzer:

- **Scopo**: File di esempio per testare l'estrazione di metadati GPS
- **Contenuto**: Dati EXIF fittizi con coordinate GPS di esempio
- **Posizione GPS**: Roma, Italia (coordinate generiche per test)
- **Sicurezza**: Sicuro da condividere - contiene solo dati di test non reali
- **Utilizzo**: Perfetto per familiarizzare con le funzionalità del tool

**Nota Importante**: Tutti i metadati nell'immagine di TEST sono fittizi e creati appositamente per scopi dimostrativi. Non rappresentano informazioni reali o sensibili.

## Limitazioni

- Le informazioni GPS sono disponibili solo se presenti nei metadati originali
- Il reverse geocoding richiede connessione internet
- Alcuni formati proprietari potrebbero avere supporto limitato
- I metadati possono essere rimossi o alterati da software di editing

## Sviluppi futuri

- [ ] Supporto per video e file multimediali
- [ ] Analisi di manipolazioni e alterazioni


## Contributi

⚠️ **IMPORTANTE**: Questo progetto ha restrizioni specifiche sui contributi.

Per contribuire:

1. **Autorizzazione preventiva**: Contatta l'autore prima di apportare modifiche
2. Fork del repository (solo dopo autorizzazione)
3. Crea un branch per la tua feature
4. Documenta dettagliatamente le modifiche nel changelog
5. Commit delle modifiche con descrizioni complete
6. Push del branch
7. Apri una Pull Request con documentazione completa

**Nota**: Tutte le modifiche devono essere approvate dall'autore e condivise sotto la stessa licenza AGPL v3.

## Licenza

🔒 **GNU AFFERO GENERAL PUBLIC LICENSE v3 + clausole specifiche**

### Restrizioni Importanti:

- ❌ **USO COMMERCIALE VIETATO** senza autorizzazione scritta
- ✅ **Uso Forense**: Permesso per forze dell'ordine e investigazioni e periti incaricati
- ✅ **Uso Accademico**: Permesso per ricerca ed educazione
- ✅ **Analisi Sicurezza**: Permesso per scopi non commerciali
- 📝 **Modifiche**: Richiedono autorizzazione preventiva dell'autore

### Contatti per Autorizzazioni:
- **Autore**: MrL-sec
- **Repository**: https://github.com/MrL-sec/GeoImageAnalyzer
- **Richieste**: Aprire una issue per autorizzazioni commerciali

Vedi il file `LICENSE` per i dettagli completi della licenza.

## Disclaimer

⚠️ **IMPORTANTE - LEGGERE ATTENTAMENTE**

Questo software è fornito "così com'è" senza garanzie di alcun tipo.

### Uso Legittimo:
- ✅ Investigazioni forensi autorizzate
- ✅ Ricerca accademica e educativa
- ✅ Analisi di sicurezza informatica
- ✅ Formazione professionale

### Uso Vietato:
- ❌ Attività illegali di qualsiasi tipo
- ❌ Violazione della privacy senza autorizzazione
- ❌ Uso commerciale non autorizzato
- ❌ Stalking o molestie

### Responsabilità:
- Gli utenti sono completamente responsabili dell'uso del software
- L'autore non è responsabile per danni derivanti dall'uso
- L'utilizzo deve essere conforme alle leggi locali e internazionali
- Il software è progettato per scopi forensi legittimi

## Supporto

Per bug report, richieste di funzionalità o supporto tecnico, apri una issue nel repository GitHub.

---

**GeoImage Analyzer v1.0** - Tool Forense Professionale per Analisi Immagini