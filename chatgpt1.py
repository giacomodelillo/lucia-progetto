import pandas as pd
import matplotlib.pyplot as plt

# 1. Caricamento dei dati
# Assumiamo che il tuo file si chiami 'data_lucia.csv'
df = pd.read_csv('data_lucia.csv')

# 2. Filtraggio e Aggregazione dei dati
# Filtriamo per 'Evento' uguale a 0
df_filtered = df[df['Evento'] == 0]

# Raggruppiamo per 'Mese' e sommiamo 'Arrivi_Stranieri'

grouped_data = df_filtered.groupby('Mese')['Arrivi_Stranieri'].sum()
# grouped_data = df.groupby('Mese')['Arrivi_Stranieri'].sum()

# Convertiamo i valori in "Migliaia" (come nel grafico di esempio)
grouped_data = grouped_data / 1000

# Ordiniamo i dati dal più piccolo al più grande per il grafico a barre orizzontali
grouped_data = grouped_data.sort_values(ascending=True)

# 3. Creazione del grafico
fig, ax = plt.subplots(figsize=(10, 6))

# Definiamo i colori: Grigio chiaro per tutti, Arancione/Bronzo per i due valori più alti
# Dato che abbiamo ordinato i dati in ordine crescente, gli ultimi due sono i maggiori
colors = ['#D3D3D3'] * len(grouped_data)  # Grigio chiaro
colors[-1] = '#D97C38'  # Colore arancione scuro (Mese maggiore)
colors[-2] = '#D97C38'  # Colore arancione scuro (Secondo mese maggiore)

# Creiamo le barre orizzontali
# Usiamo .astype(str) sull'indice per trattare i mesi come etichette e non numeri
bars = ax.barh(grouped_data.index.astype(str), grouped_data.values, color=colors)

# 4. Personalizzazione estetica (per renderlo simile all'immagine)
# Titolo principale
fig.text(0.12, 0.95, "For 'Evento: 0', 'Mese': 8 and 6 have noticeably higher 'Arrivi_Stranieri'.", 
         fontsize=14, color='#333333')

# Sottotitolo
ax.set_title("Sum of Arrivi_Stranieri (Thousands)", loc='left', fontsize=10, pad=10)

# Etichette assi
ax.set_ylabel("Mese", fontsize=12)
ax.set_xlabel("") # Rimuoviamo etichetta asse X per pulizia

# Rimuovere i bordi (spines) superiore e destro
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')
ax.spines['left'].set_color('#DDDDDD')

# Aggiungere griglia verticale leggera
ax.xaxis.grid(True, color='#EEEEEE')
ax.set_axisbelow(True) # Mette la griglia dietro le barre

# Mostra il grafico
plt.tight_layout(rect=[0, 0, 1, 0.95]) # Lascia spazio per il titolo in alto
plt.show()