import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io



df = pd.read_csv('Data-Management-3-2.csv')

# 2. Pulizia e Calcoli
df = df[~df['Anno'].isin([2020, 2021])] # Esclusione anni Covid
df['Arrivi_Totali'] = df['Arrivi_Italiani'] + df['Arrivi_Stranieri']
df['Presenze_Totali'] = df['Presenze_Italiani'] + df['Presenze_Stranieri']
df['Durata'] = df['Presenze_Totali'] / df['Arrivi_Totali']

# 3. Preparazione dei dati raggruppati
# Calcoliamo le medie per i due gruppi
grouped = df.groupby('Evento').mean(numeric_only=True)[['Arrivi_Totali', 'Durata']]

labels = ['No Eventi', 'Sì Eventi']
arrivi_means = grouped['Arrivi_Totali'].values
durata_means = grouped['Durata'].values

x = np.arange(len(labels))  # Posizioni delle etichette
width = 0.35  # Larghezza delle barre

# 4. Creazione del Grafico Unico con Doppio Asse Y
fig, ax1 = plt.subplots(figsize=(10, 7))

# --- BARRE 1: ARRIVI (Asse Sinistro - Blu) ---
rects1 = ax1.bar(x - width/2, arrivi_means, width, label='Media Arrivi', color='#1f77b4', alpha=0.9, edgecolor='black')
ax1.set_ylabel('Numero di Arrivi', color='#1f77b4', fontsize=12, fontweight='bold')
ax1.set_title('Confronto Diretto: Arrivi vs Durata Soggiorno\n(Raggruppato per Presenza Eventi)', fontsize=14)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, fontsize=12)
ax1.tick_params(axis='y', labelcolor='#1f77b4')

# --- BARRE 2: DURATA (Asse Destro - Arancione) ---
ax2 = ax1.twinx()  # Crea un secondo asse Y che condivide lo stesso asse X
rects2 = ax2.bar(x + width/2, durata_means, width, label='Media Durata', color='#ff7f0e', alpha=0.9, edgecolor='black')
ax2.set_ylabel('Durata Media (Giorni)', color='#ff7f0e', fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#ff7f0e')

# Impostiamo i limiti dell'asse Y per "dare aria" alle barre
ax1.set_ylim(0, max(arrivi_means) * 1.2)
ax2.set_ylim(0, max(durata_means) * 1.2)

# --- Aggiunta delle Etichette Valori sopra le barre ---
def autolabel(rects, ax, format_str):
    """Funzione per attaccare un'etichetta con il valore sopra ogni barra"""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(format_str.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 punti di offset verticale
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold')

autolabel(rects1, ax1, "{:,.0f}")  # Formato intero per Arrivi
autolabel(rects2, ax2, "{:.2f} gg") # Formato decimale per Giorni

# Legenda unica combinata
lines, labels_l = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels_l + labels2, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)

fig.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.show()