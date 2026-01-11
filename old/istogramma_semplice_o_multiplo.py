import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Impostazione del tema
plt.style.use('seaborn-v0_8-muted')

# ==============================================================================
# 1. LIBRERIA PRESET (MAPPATURE)
# ==============================================================================
PRESET_MAPPATURE = {
    'NESSUNO': {},
    
    'MESI': {
        1: 'Gennaio', 2: 'Febbraio', 3: 'Marzo', 4: 'Aprile',
        5: 'Maggio', 6: 'Giugno', 7: 'Luglio', 8: 'Agosto',
        9: 'Settembre', 10: 'Ottobre', 11: 'Novembre', 12: 'Dicembre'
    },
    
    'GIORNI_SETTIMANA': {
        1: 'Lunedì', 2: 'Martedì', 3: 'Mercoledì', 4: 'Giovedì',
        5: 'Venerdì', 6: 'Sabato', 7: 'Domenica'
    },
    
    'TRIMESTRI': {
        1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'
    }
}

# ==============================================================================
# 2. CONFIGURAZIONE TEMPLATE (MODIFICA QUI)
# ==============================================================================

# --- FILE E DATI ---
FILE_PATH = 'data_lucia.csv'

# --- CONFIGURAZIONE ASSI ---
COLONNA_X = 'Mese' 

# Asse Y: Lista delle colonne da visualizzare (una barra per ognuna)
COLONNE_Y = [
    'Arrivi_Italiani', 
    'Arrivi_Stranieri',
    'Presenze_Italiani',
    'Presenze_Stranieri'

]

# --- PRESET ETICHETTE ASSE X (NOVITÀ) ---
# Scegli: 'NESSUNO', 'MESI', 'GIORNI_SETTIMANA', 'TRIMESTRI'
NOME_PRESET = 'MESI'

# --- CONFIGURAZIONE ETICHETTE NUMERI ---
# Opzioni: 'center' (dentro, bianco), 'top' (sopra, nero), 'none' (nascosto)
POSIZIONI_LABEL = [
    'top',       # Per la prima colonna (Italiani)
    'center'     # Per la seconda colonna (Stranieri)
]
ROTAZIONE_LABEL = 90  # 90 = Verticale, 0 = Orizzontale

# --- LOGICA DI CALCOLO ---
# True = MEDIA, False = SOMMA TOTALE
CALCOLA_MEDIA = False 

# --- ESTETICA ---
COLORI = ['#4c72b0', '#dd8452', '#55a868', '#c44e52'] 
NOMI_LEGENDA = ["Italiani", "Stranieri"] # Lascia [] se vuoi i nomi originali

TITOLO_GRAFICO = 'Confronto Arrivi: Italiani vs Stranieri'
DISTANZA_TITOLO = 40
TITOLO_ASSE_X  = 'Mese'
TITOLO_ASSE_Y  = 'Totale Arrivi'

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

if CALCOLA_MEDIA:
    df_grouped = df.groupby(COLONNA_X)[COLONNE_Y].mean().reset_index()
else:
    df_grouped = df.groupby(COLONNA_X)[COLONNE_Y].sum().reset_index()

df_grouped = df_grouped.sort_values(by=COLONNA_X)

mappa = PRESET_MAPPATURE.get(NOME_PRESET, {})
if mappa:
    df_grouped[COLONNA_X] = df_grouped[COLONNA_X].replace(mappa)

plt.figure(figsize=(12, 8))

labels = df_grouped[COLONNA_X].astype(str)
x = np.arange(len(labels))
num_vars = len(COLONNE_Y)
width_total = 0.85
width_bar = width_total / num_vars

for i, col_name in enumerate(COLONNE_Y):

    position = x - (width_total / 2) + (i * width_bar) + (width_bar / 2)
    
    valori = df_grouped[col_name]
    colore = COLORI[i % len(COLORI)]
    label_legenda = NOMI_LEGENDA[i] if len(NOMI_LEGENDA) > i else col_name
    
   
    pos_label = POSIZIONI_LABEL[i] if i < len(POSIZIONI_LABEL) else 'top'

    rects = plt.bar(position, valori, width_bar, label=label_legenda, color=colore, edgecolor='white')
    

    if pos_label != 'none':
        for rect in rects:
            height = rect.get_height()
            
            if height > 0:
                fmt = '{:,.0f}' if not CALCOLA_MEDIA else '{:,.1f}'
                
                
                if pos_label == 'center':
                    xy_pos = (rect.get_x() + rect.get_width() / 2, height / 2)
                    xy_offset = (0, 0)
                    va_align = 'center'
                    txt_color = 'white'
                else: # 'top'
                    xy_pos = (rect.get_x() + rect.get_width() / 2, height)
                    xy_offset = (0, 5) 
                    va_align = 'bottom'
                    txt_color = 'black'

                plt.annotate(fmt.format(height),
                            xy=xy_pos,
                            xytext=xy_offset,
                            textcoords="offset points",
                            ha='center', va=va_align,
                            fontsize=9, 
                            color=txt_color, 
                            fontweight='bold', 
                            rotation=ROTAZIONE_LABEL)

# --- FINITURE ---
plt.title(TITOLO_GRAFICO, fontsize=16, fontweight='bold', pad=DISTANZA_TITOLO)
plt.xlabel(TITOLO_ASSE_X, fontsize=13, labelpad=10)
plt.ylabel(TITOLO_ASSE_Y, fontsize=13, labelpad=10)
plt.xticks(x, labels)
plt.legend(fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()