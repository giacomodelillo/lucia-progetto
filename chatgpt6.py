import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# 1. Caricamento Dati
df = pd.read_csv('data_lucia.csv')

# --- CORREZIONE ERRORE ---
# Creiamo la data mappando manualmente le colonne italiane in quelle inglesi
df['Data_Leggibile'] = pd.to_datetime({
    'year': df['Anno'],
    'month': df['Mese'],
    'day': 1
})

# Calcoliamo il totale turisti
df['Totale_Arrivi'] = df['Arrivi_Italiani'] + df['Arrivi_Stranieri']

# 2. Calcolo della Regressione (NumPy)
# X: numeri progressivi (0, 1, 2...)
x = np.arange(len(df))
# Y: i dati reali
y = df['Totale_Arrivi']

# Calcolo pendenza (m) e intercetta (q)
m, q = np.polyfit(x, y, 1)

# Creazione della linea di trend
trend_line = (m * x) + q

# 3. Creazione del Grafico
fig, ax = plt.subplots(figsize=(12, 6))

# A. Scatter plot (Dati reali)
ax.scatter(df['Data_Leggibile'], y, color='#4c72b0', alpha=0.5, label='Dati Reali')

# B. Linea di Regressione
ax.plot(df['Data_Leggibile'], trend_line, color='#c44e52', linewidth=3, label='Trend Lineare')

# 4. Estetica
ax.set_title(f'Trend Generale Arrivi (Variazione media: {m:+.0f} al mese)', fontsize=15, fontweight='bold', color='#333333')
ax.set_ylabel('Totale Arrivi', fontsize=12)

# Griglia e bordi
ax.grid(True, color='#EEEEEE', linestyle='-')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Formattazione numeri asse Y (Migliaia)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))

plt.legend()
plt.tight_layout()
plt.show()

print(f"Fatto. Pendenza calcolata (m): {m:.2f}")