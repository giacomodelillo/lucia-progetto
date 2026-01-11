import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Impostazione del tema
plt.style.use('seaborn-v0_8-muted')

# ==============================================================================
# 1. CONFIGURAZIONE TEMPLATE (MODIFICA QUI)
# ==============================================================================

FILE_PATH = 'Data-Management-3-2.csv'

# --- ASSI ---
COLONNA_X = 'Mese' 
COLONNE_Y = [
    'Arrivi_Italiani', 
    'Arrivi_Stranieri' 
    # L'ordine conta: il primo è in basso (base), l'ultimo in alto
]

# --- PRESET ETICHETTE X ---
PRESET_MAPPATURE = {
    'NESSUNO': {},
    'MESI': {1: 'Gen', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mag', 6: 'Giu', 
             7: 'Lug', 8: 'Ago', 9: 'Set', 10: 'Ott', 11: 'Nov', 12: 'Dic'},
}
NOME_PRESET = 'MESI'

# --- CONFIGURAZIONE ETICHETTE (NOVITÀ) ---

# 1. Numeri INTERNI (i segmenti colorati)
POSIZIONE_VALORI_INTERNI = 'center'  # 'center' o 'none'
ROTAZIONE_INTERNA = 90               # 90 = Verticale, 0 = Orizzontale
SOGLIA_MINIMA_LABEL = 1000           # Non scrive il numero se il segmento è troppo piccolo

# 2. Numero TOTALE (somma in cima alla barra)
MOSTRA_TOTALE_CIMA = True            # True = Mostra somma, False = Nascondi

# --- ESTETICA ---
TITOLO_GRAFICO = 'Composizione Arrivi Totali (Stacked)'
DISTANZA_TITOLO = 40
TITOLO_ASSE_X  = 'Mese'
TITOLO_ASSE_Y  = 'Totale Cumulativo'
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


plt.figure(figsize=(12, 8))

labels = labels_x
x = np.arange(len(labels))
width = 0.65


bottom = np.zeros(len(labels))

for i, col in enumerate(COLONNE_Y):
    valori = df_grouped[col].values
    colore = COLORI[i % len(COLORI)]
    
   
    bars = plt.bar(x, valori, width, label=col, color=colore, bottom=bottom, edgecolor='white')
    
   
    if POSIZIONE_VALORI_INTERNI == 'center':
        for bar, val in zip(bars, valori):
            if val > SOGLIA_MINIMA_LABEL: 
               
                y_center = bar.get_y() + bar.get_height() / 2
                
                plt.text(bar.get_x() + bar.get_width()/2, y_center, 
                         f'{val:,.0f}', 
                         ha='center', va='center', 
                         color='white', fontsize=10, fontweight='bold',
                         rotation=ROTAZIONE_INTERNA) 
    

    bottom += valori


if MOSTRA_TOTALE_CIMA:
    for i, tot in enumerate(bottom):
        plt.text(x[i], tot, 
                 f'{tot:,.0f}', 
                 ha='center', va='bottom', 
                 fontweight='bold', color='black', fontsize=11)

# --- FINITURE ---
plt.title(TITOLO_GRAFICO, fontsize=16, fontweight='bold', pad=DISTANZA_TITOLO)
plt.xlabel(TITOLO_ASSE_X, fontsize=13, labelpad=10)
plt.ylabel(TITOLO_ASSE_Y, fontsize=13, labelpad=10)
plt.xticks(x, labels)


plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Legenda") 
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()