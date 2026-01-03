import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Impostazione del tema
plt.style.use('seaborn-v0_8-muted')

# ==============================================================================
# 1. LIBRERIA PRESET (MAPPATURE)
# ==============================================================================
# Qui definisci come tradurre i numeri (0 e 1) in testo
PRESET_MAPPATURE = {
    'NESSUNO': {}, # Usa "Gruppo 0" e "Gruppo 1" o manuali
    
    'EVENTI_BOOLEANI': {
        0: 'Eventi Assenti', 
        1: 'Eventi Presenti'
    },
    
    'SI_NO': {
        0: 'No', 
        1: 'Sì'
    },
    
    'MASCHIO_FEMMINA': {
        0: 'Maschi', 
        1: 'Femmine'
    },
    
    'WEEKEND': {
        0: 'Giorni Feriali', 
        1: 'Weekend'
    }
}

# ==============================================================================
# 2. CONFIGURAZIONE UTENTE (MODIFICA QUI)
# ==============================================================================

# --- FILE E DATI ---
FILE_PATH = 'Data-Management-3-2.csv'

# Quali colonne vuoi analizzare? (Verranno SOMMATE tra loro)
COLONNE_DA_SOMMARE = [
    'Arrivi_Italiani', 
    'Arrivi_Stranieri'
]

# La colonna che fa da discriminante (deve contenere 0 e 1)
COLONNA_BOOLEANA = 'Evento'

# --- SCELTA PRESET ---
# Scrivi qui il nome del preset da usare (vedi lista sopra)
NOME_PRESET = 'EVENTI_BOOLEANI' 

# --- MODALITÀ GRAFICO ---
# True  = BOXPLOT (Distribuzione statistica)
# False = ISTOGRAMMA (Somma Totale)
USA_BOXPLOT = False

# --- CONFIGURAZIONE ETICHETTE (SOLO PER ISTOGRAMMA) ---
POSIZIONE_LABEL = 'center' # 'center' (dentro, bianco), 'top' (sopra, nero), 'none'
ROTAZIONE_LABEL = 0        # 0 orizzontale, 90 verticale

# --- ESTETICA E TITOLI ---
TITOLO_GRAFICO = 'Analisi Impatto Eventi sui Flussi Turistici'
DISTANZA_TITOLO = 30       # Spazio extra tra titolo e grafico
TITOLO_ASSE_X  = 'Stato'
TITOLO_ASSE_Y  = 'Totale Arrivi'

# Colori
COLORE_0  = '#51a2ff'  # Colore per il gruppo 0 (es. No Evento)
COLORE_1  = '#a684ff'  # Colore per il gruppo 1 (es. Sì Evento)

# ==============================================================================
try:
    df = pd.read_csv(FILE_PATH, thousands=',', on_bad_lines='skip')
except FileNotFoundError:
    print(f"ERRORE CRITICO: Il file '{FILE_PATH}' non è stato trovato.")
    exit()

for col in COLONNE_DA_SOMMARE:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(r'[^\d\.]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    else:
        print(f"ATTENZIONE: La colonna '{col}' non esiste nel CSV.")

df['Variabile_Analisi'] = df[COLONNE_DA_SOMMARE].sum(axis=1)

df = df[df[COLONNA_BOOLEANA].notnull()]
df[COLONNA_BOOLEANA] = df[COLONNA_BOOLEANA].astype(int)

data_0 = df[df[COLONNA_BOOLEANA] == 0]['Variabile_Analisi']
data_1 = df[df[COLONNA_BOOLEANA] == 1]['Variabile_Analisi']

mappa = PRESET_MAPPATURE.get(NOME_PRESET, {})
label_0 = mappa.get(0, "Gruppo 0") 
label_1 = mappa.get(1, "Gruppo 1") 


plt.figure(figsize=(9, 7))

etichette = [label_0, label_1]
colori = [COLORE_0, COLORE_1]

if USA_BOXPLOT:

    print(f"Generazione Boxplot ({label_0} vs {label_1})")
    
    bplot = plt.boxplot([data_0, data_1], 
                        labels=etichette, 
                        patch_artist=True,
                        medianprops=dict(color="black", linewidth=1.5),
                        widths=0.6)

    for patch, color in zip(bplot['boxes'], colori):
        patch.set_facecolor(color)
        patch.set_alpha(0.85)

 
    for i, d in enumerate([data_0, data_1]):
        y = d
        x = np.random.normal(1 + i, 0.04, size=len(y))
        plt.scatter(x, y, alpha=0.4, color='black', s=15, zorder=10)

else:
    print(f"Generazione Istogramma Somme ({label_0} vs {label_1})")
    
    valori = [data_0.sum(), data_1.sum()]
    
    bars = plt.bar(etichette, valori, color=colori, edgecolor='white', width=0.6)

    if POSIZIONE_LABEL != 'none':
        for bar in bars:
            height = bar.get_height()
            
           
            if POSIZIONE_LABEL == 'center':
                xy_pos = (bar.get_x() + bar.get_width() / 2, height / 2)
                xy_offset = (0, 0)
                va_align = 'center'
                txt_color = 'white'
            else: 
                xy_pos = (bar.get_x() + bar.get_width() / 2, height)
                xy_offset = (0, 5)
                va_align = 'bottom'
                txt_color = 'black'

            if height > 0:
                plt.annotate(f'{height:,.0f}',
                            xy=xy_pos,
                            xytext=xy_offset,
                            textcoords="offset points",
                            ha='center', va=va_align,
                            fontsize=12, 
                            color=txt_color, 
                            fontweight='bold', 
                            rotation=ROTAZIONE_LABEL)

# --- FINITURE GRAFICO ---
plt.title(TITOLO_GRAFICO, fontsize=16, fontweight='bold', pad=DISTANZA_TITOLO)
plt.xlabel(TITOLO_ASSE_X, fontsize=13, labelpad=10)
plt.ylabel(TITOLO_ASSE_Y, fontsize=13, labelpad=10)


plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()