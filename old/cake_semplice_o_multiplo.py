import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Impostazione del tema
plt.style.use('seaborn-v0_8-muted')

# ==============================================================================
# 1. LIBRERIA PRESET (NON MODIFICARE QUI, SCEGLI SOTTO)
# ==============================================================================
PRESET_MAPPATURE = {
    'NESSUNO': {}, # Usa i valori originali del file

    'MESI': {
        1: 'Gennaio', 2: 'Febbraio', 3: 'Marzo', 4: 'Aprile',
        5: 'Maggio', 6: 'Giugno', 7: 'Luglio', 8: 'Agosto',
        9: 'Settembre', 10: 'Ottobre', 11: 'Novembre', 12: 'Dicembre'
    },

    'GIORNI_SETTIMANA': {
        1: 'Lunedì', 2: 'Martedì', 3: 'Mercoledì', 4: 'Giovedì',
        5: 'Venerdì', 6: 'Sabato', 7: 'Domenica'
    },

    'EVENTI_BOOLEANI': {
        0: 'Nessun Evento',
        1: 'Evento Presente'
    },

    'TRIMESTRI': {
        1: 'Q1 (Gen-Mar)', 2: 'Q2 (Apr-Giu)',
        3: 'Q3 (Lug-Set)', 4: 'Q4 (Ott-Dic)'
    }
}

# ==============================================================================
# 2. CONFIGURAZIONE UTENTE (MODIFICA QUI)
# ==============================================================================

# --- FILE E DATI ---
FILE_PATH = 'data_lucia.csv'

# --- SELEZIONE COLONNE ---
COLONNA_CATEGORIA = 'Mese'   # Es. 'Mese', 'Evento'
COLONNE_VALORI = [
    'Arrivi_Italiani',
    'Arrivi_Stranieri'
]

# --- SCELTA PRESET (NOVITÀ) ---
# Scrivi qui il nome del preset da usare (vedi lista sopra):
# Opzioni: 'NESSUNO', 'MESI', 'GIORNI_SETTIMANA', 'EVENTI_BOOLEANI', 'TRIMESTRI'
NOME_PRESET = 'MESI'

# --- OPZIONI AVANZATE ---
SOGLIA_CUTOFF = 2.5    # % sotto la quale finisce in "Altro"
STILE_CIAMBELLA = True # True = Ciambella, False = Torta piena
ETICHETTA_ALTRO = "Altri"

# --- LEGENDA ---
MOSTRA_LEGENDA = True
TITOLO_LEGENDA = "Periodo"

# --- ESTETICA ---
TITOLO_GRAFICO = 'Distribuzione Totale Arrivi per Mese'
DISTANZA_TITOLO = 40  # Aumenta questo numero se il titolo tocca il grafico
COLORE_TESTO_PCT = 'white'

# ==============================================================================
# 3. CARICAMENTO E PREPARAZIONE DATI
# ==============================================================================
try:
    df = pd.read_csv(FILE_PATH, thousands=',', on_bad_lines='skip')
except FileNotFoundError:
    print(f"ERRORE: File '{FILE_PATH}' non trovato.")
    exit()

# 1. Pulizia e Mappatura Colonna Categoria
# Convertiamo in numero se possibile per applicare il preset (es. 1 -> Gennaio)
if pd.api.types.is_numeric_dtype(df[COLONNA_CATEGORIA]) or df[COLONNA_CATEGORIA].astype(str).str.isnumeric().all():
    df[COLONNA_CATEGORIA] = pd.to_numeric(df[COLONNA_CATEGORIA], errors='coerce').fillna(0).astype(int)

# --- APPLICAZIONE PRESET ---
dizionario_scelto = PRESET_MAPPATURE.get(NOME_PRESET, {})
if dizionario_scelto:
    print(f"Sto applicando il preset: {NOME_PRESET}")
    df[COLONNA_CATEGORIA] = df[COLONNA_CATEGORIA].replace(dizionario_scelto)

# Convertiamo in stringa per il grafico
df[COLONNA_CATEGORIA] = df[COLONNA_CATEGORIA].astype(str)

# 2. Pulizia Colonne Valori
for col in COLONNE_VALORI:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(r'[^\d\.]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# 3. Calcolo Totale e Raggruppamento
df['Valore_Totale'] = df[COLONNE_VALORI].sum(axis=1)
df_grouped = df.groupby(COLONNA_CATEGORIA)['Valore_Totale'].sum().reset_index()

# 4. Logica Cutoff "Altro"
totale_generale = df_grouped['Valore_Totale'].sum()
df_grouped['Percentuale'] = (df_grouped['Valore_Totale'] / totale_generale) * 100

df_main = df_grouped[df_grouped['Percentuale'] >= SOGLIA_CUTOFF].copy()
df_small = df_grouped[df_grouped['Percentuale'] < SOGLIA_CUTOFF].copy()

if not df_small.empty:
    valore_altro = df_small['Valore_Totale'].sum()
    row_altro = pd.DataFrame({
        COLONNA_CATEGORIA: [ETICHETTA_ALTRO],
        'Valore_Totale': [valore_altro],
        'Percentuale': [(valore_altro / totale_generale) * 100]
    })
    df_final = pd.concat([df_main, row_altro], ignore_index=True)
else:
    df_final = df_main

df_final = df_final.sort_values(by='Valore_Totale', ascending=False)

# ==============================================================================
# 4. GENERAZIONE GRAFICO
# ==============================================================================
plt.figure(figsize=(12, 8))

labels = df_final[COLONNA_CATEGORIA]
sizes = df_final['Valore_Totale']

# Creazione Torta
wedges, texts, autotexts = plt.pie(sizes,
                                   labels=labels,
                                   autopct='%1.1f%%',
                                   startangle=140,
                                   pctdistance=0.82 if STILE_CIAMBELLA else 0.6,
                                   textprops={'fontsize': 11})

# Stile numeri percentuali
for autotext in autotexts:
    autotext.set_color(COLORE_TESTO_PCT)
    autotext.set_weight('bold')
    autotext.set_fontsize(10)

# Stile etichette esterne
for text in texts:
    text.set_fontsize(11)

# Effetto Ciambella
if STILE_CIAMBELLA:
    centre_circle = plt.Circle((0,0),0.65,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

# Legenda (Spostata a destra)
if MOSTRA_LEGENDA:
    plt.legend(wedges, labels,
               title=TITOLO_LEGENDA,
               loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1), # Fuori a destra
               fontsize=10,
               title_fontsize=12)

# Titolo con padding aumentato
plt.title(TITOLO_GRAFICO, fontsize=16, fontweight='bold', pad=DISTANZA_TITOLO)

plt.axis('equal')
plt.tight_layout()
plt.show()
