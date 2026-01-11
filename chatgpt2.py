import pandas as pd
import matplotlib.pyplot as plt

# 1. Caricamento dei dati
df = pd.read_csv('data_lucia.csv')

# 2. Elaborazione dei dati
# Raggruppiamo per 'Anno' ed 'Evento' sommando le 'Presenze_Stranieri'
# Usiamo pivot_table per avere gli anni come righe e l'Evento (0 e 1) come colonne
df_pivot = df.pivot_table(index='Anno', columns='Evento', values='Presenze_Stranieri', aggfunc='sum')

# Convertiamo in migliaia (diviso 1000) per corrispondere alla scala dell'asse Y (0 - 7000)
df_pivot = df_pivot / 1000

# 3. Creazione del grafico
fig, ax = plt.subplots(figsize=(10, 5))

# Disegniamo le linee
# Linea Blu (corrisponde a Evento 0 nel tuo grafico: picco nel 2018)
ax.plot(df_pivot.index, df_pivot[0], color='#2F557F', linewidth=2, label='Evento 0')

# Linea Arancione (corrisponde a Evento 1 nel tuo grafico: calo nel 2018, picco nel 2019)
ax.plot(df_pivot.index, df_pivot[1], color='#D97C38', linewidth=2, label='Evento 1')

# 4. Personalizzazione estetica (Stile "Clean")
# Griglia orizzontale leggera
ax.yaxis.grid(True, color='#EEEEEE', linestyle='-')
ax.xaxis.grid(False)

# Rimuovere i bordi (spines)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False) # Nel grafico di esempio l'asse Y non ha la linea verticale
ax.spines['bottom'].set_color('#DDDDDD')

# Rimuovere i trattini (ticks) dagli assi ma tenere le etichette
ax.tick_params(axis='both', which='both', length=0)

# Impostare limiti e etichette
ax.set_xlabel("Anno", fontsize=10, labelpad=10, color='#555555')
# L'asse Y parte da 0 e arriva circa a 7000
ax.set_ylim(0, 7000)

# Aggiungere la legenda (opzionale, basata sui colori)
# plt.legend() 

plt.tight_layout()
plt.show()