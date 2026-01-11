import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Impostazione del tema
plt.style.use('seaborn-v0_8-muted')

# ==============================================================================
# 1. CONFIGURAZIONE TEMPLATE
# ==============================================================================

FILE_PATH = 'Data-Management-3-2.csv'

# --- ASSI ---
COLONNA_X = 'Mese' # Es. 'Mese', 'Anno', 'Giorno'

# Liste delle linee da disegnare
COLONNE_Y = [
    'Arrivi_Italiani',
    'Arrivi_Stranieri'
]

# --- LIBRERIA PRESET (MAPPATURA X) ---
PRESET_MAPPATURE = {
    'NESSUNO': {},
    'MESI': {1: 'Gen', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mag', 6: 'Giu', 
             7: 'Lug', 8: 'Ago', 9: 'Set', 10: 'Ott', 11: 'Nov', 12: 'Dic'},
}
NOME_PRESET = 'MESI' 

# --- OPZIONI VISIVE ---
MOSTRA_PUNTI = True     # Mostra i pallini sui dati
RIEMPI_AREA = True     # True = Area Chart (colora sotto la linea)
SPESSORE_LINEA = 2.5
GRIGLIA_VERTICALE = True

# --- ESTETICA ---
TITOLO_GRAFICO = 'Andamento Stagionale Arrivi'
TITOLO_ASSE_X  = 'Mese'
TITOLO_ASSE_Y  = 'Numero Arrivi'
DISTANZA_TITOLO = 30
COLORI = ['#4c72b0', '#dd8452', '#55a868', '#c44e52'] 

# ==============================================================================

try:
    df = pd.read_csv(FILE_PATH, thousands=',', on_bad_lines='skip')
except FileNotFoundError:
    print(f"ERRORE: File '{FILE_PATH}' non trovato.")
    exit()

if pd.api.types.is_numeric_dtype(df[COLONNA_X]) or df[COLONNA_X].astype(str).str.isnumeric().all():
    df = df[pd.to_numeric(df[COLONNA_X], errors='coerce').notnull()]
    df[COLONNA_X] = df[COLONNA_X].astype(int)

for col in COLONNE_Y:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(r'[^\d\.]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

df_grouped = df.groupby(COLONNA_X)[COLONNE_Y].sum().reset_index()
df_grouped = df_grouped.sort_values(by=COLONNA_X)

mappa = PRESET_MAPPATURE.get(NOME_PRESET, {})
if mappa:
    labels_x = df_grouped[COLONNA_X].replace(mappa).astype(str)
else:
    labels_x = df_grouped[COLONNA_X].astype(str)

plt.figure(figsize=(12, 7))

x_pos = np.arange(len(labels_x))

for i, col in enumerate(COLONNE_Y):
    y_val = df_grouped[col]
    colore = COLORI[i % len(COLORI)]
    
    plt.plot(x_pos, y_val, 
             label=col, 
             color=colore, 
             linewidth=SPESSORE_LINEA,
             marker='o' if MOSTRA_PUNTI else None,
             markersize=8)
    
    if RIEMPI_AREA:
        plt.fill_between(x_pos, y_val, color=colore, alpha=0.1)
        
    last_y = y_val.iloc[-1]
    plt.annotate(f'{last_y:,.0f}', 
                 xy=(x_pos[-1], last_y), 
                 xytext=(5, 0), textcoords='offset points', 
                 color=colore, fontweight='bold')

# --- FINITURE ---
plt.title(TITOLO_GRAFICO, fontsize=16, fontweight='bold', pad=DISTANZA_TITOLO)
plt.xlabel(TITOLO_ASSE_X, fontsize=13, labelpad=10)
plt.ylabel(TITOLO_ASSE_Y, fontsize=13, labelpad=10)

plt.xticks(x_pos, labels_x)
plt.legend(fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.5)
if GRIGLIA_VERTICALE:
    plt.grid(axis='x', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()