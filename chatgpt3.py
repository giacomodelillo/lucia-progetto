import pandas as pd
import matplotlib.pyplot as plt

# 1. Caricamento e Preparazione dei dati
file_path = 'data_lucia.csv'
df = pd.read_csv(file_path)

# Colonne da visualizzare
colonne_y = [
    'Arrivi_Italiani', 
    'Arrivi_Stranieri',
    'Presenze_Italiani',
    'Presenze_Stranieri'
]

# Raggruppiamo per 'Mese' e sommiamo i valori
df_grouped = df.groupby('Mese')[colonne_y].sum()

# Mappatura dei nomi dei mesi per l'asse X (più leggibile)
nomi_mesi = {1: 'Gen', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mag', 6: 'Giu', 
             7: 'Lug', 8: 'Ago', 9: 'Set', 10: 'Ott', 11: 'Nov', 12: 'Dic'}
df_grouped.index = df_grouped.index.map(nomi_mesi)

# 2. Creazione del Grafico
fig, ax = plt.subplots(figsize=(14, 7))

# Definizione colori (Palette distinta e moderna)
colors = ['#4c72b0', '#dd8452', '#55a868', '#c44e52'] 

# Disegno delle barre raggruppate
# width=0.85 rende le barre vicine tra loro, edgecolor='white' le separa visivamente
df_grouped.plot(kind='bar', ax=ax, width=0.85, color=colors, edgecolor='white', linewidth=0.7)

# 3. Personalizzazione Estetica (Stile "Clean")

# Titolo e etichette
ax.set_title('Confronto Mensile: Arrivi e Presenze (Totali)', fontsize=16, pad=20, color='#333333', fontweight='bold')
ax.set_xlabel('') # Rimuoviamo "Mese" perché i nomi (Gen, Feb...) sono ovvi
ax.set_ylabel('Numero di Persone', fontsize=11, color='#555555')

# Griglia leggera solo orizzontale
ax.yaxis.grid(True, color='#EEEEEE', linestyle='-')
ax.xaxis.grid(False)
ax.set_axisbelow(True) # Mette la griglia dietro le barre

# Rimozione bordi pesanti (spines)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False) # Rimuoviamo la linea verticale asse Y
ax.spines['bottom'].set_color('#CCCCCC')

# Formattazione testi assi
plt.xticks(rotation=0, fontsize=11, color='#333333') # Rotazione 0 per leggere bene i mesi
plt.yticks(fontsize=10, color='#555555')
ax.tick_params(axis='both', which='both', length=0) # Rimuove i trattini degli assi

# Legenda pulita in alto a sinistra
plt.legend(title='', loc='upper left', ncol=4, frameon=False, fontsize=10)

# Formattazione asse Y con separatore migliaia (es. 1,000,000)
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

plt.tight_layout()
plt.show()