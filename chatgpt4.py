import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Caricamento e Calcoli
df = pd.read_csv('data_lucia.csv')

# Calcoliamo il totale turisti (Italiani + Stranieri) per ogni riga
df['Totale_Arrivi'] = df['Arrivi_Italiani'] + df['Arrivi_Stranieri']

# Raggruppiamo per mese calcolando la MEDIA
df_pie = df.groupby('Mese')['Totale_Arrivi'].mean()

# Nomi mesi per le etichette
labels = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 
          'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic']

# 2. Configurazione Estetica
# Creiamo una lista per "esplodere" (staccare) la fetta più grande
max_idx = df_pie.idxmax() - 1  # Indice del valore massimo (sottraiamo 1 perché i mesi partono da 1)
explode = [0] * 12
explode[max_idx] = 0.1  # Stacca la fetta maggiore del 10%

# Colori: usiamo una palette spettrale per differenziare i 12 mesi
colors = plt.cm.Set3(np.linspace(0, 1, 12))

# 3. Creazione del Grafico
fig, ax = plt.subplots(figsize=(10, 8))

# Disegno della torta
wedges, texts, autotexts = ax.pie(df_pie, 
                                  explode=explode, 
                                  labels=labels, 
                                  colors=colors, 
                                  autopct='%1.1f%%', # Mostra la percentuale
                                  startangle=90,     # Ruota per avere Gennaio in alto o il primo quadrante
                                  pctdistance=0.85,  # Distanza percentuale dal centro
                                  shadow=False)

# 4. Trasformazione in "Ciambella" (Donut Chart)
# Aggiungiamo un cerchio bianco al centro
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

# 5. Personalizzazione Testi
plt.setp(texts, size=11, color="#333333")       # Etichette mesi (esterne)
plt.setp(autotexts, size=10, weight="bold", color="#444444") # Percentuali (interne)

# Titolo
plt.title('Distribuzione Media Mensile degli Arrivi Totali', fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.show()