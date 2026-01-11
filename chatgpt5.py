import pandas as pd
import matplotlib.pyplot as plt

# 1. Caricamento e Preparazione
file_path = 'data_lucia.csv'
df = pd.read_csv(file_path)

# Calcoliamo il totale turisti (Arrivi)
df['Totale_Turisti'] = df['Arrivi_Italiani'] + df['Arrivi_Stranieri']

# Separiamo i dati in due gruppi
no_evento = df[df['Evento'] == 0]['Totale_Turisti']
si_evento = df[df['Evento'] == 1]['Totale_Turisti']

# Calcoliamo le medie per visualizzarle
media_no = no_evento.mean()
media_si = si_evento.mean()
incremento = ((media_si - media_no) / media_no) * 100

# 2. Creazione del Grafico
fig, ax = plt.subplots(figsize=(10, 7))

# Dati da plottare
data_to_plot = [no_evento, si_evento]

# Creazione del Box Plot
# patch_artist=True permette di riempire le scatole di colore
bp = ax.boxplot(data_to_plot, patch_artist=True, widths=0.6, 
                labels=['Nessun Evento (0)', 'Evento Presente (1)'],
                showmeans=True, meanline=True)

# 3. Personalizzazione Colori
colors = ['#2F557F', '#D97C38'] # Blu (No) e Arancione (Sì) - Stile precedente

for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)       # Colore riempimento
    patch.set_alpha(0.7)             # Trasparenza
    patch.set_edgecolor(color)       # Colore bordo
    patch.set_linewidth(2)

# Personalizzazione degli altri elementi del boxplot (baffi, mediane, outlier)
plt.setp(bp['whiskers'], color='#555555', linewidth=1.5)
plt.setp(bp['caps'], color='#555555', linewidth=1.5)
plt.setp(bp['medians'], color='white', linewidth=2)       # Mediana bianca solida
plt.setp(bp['means'], color='yellow', linewidth=2, linestyle='--') # Media tratteggiata gialla
plt.setp(bp['fliers'], markeredgecolor='#555555', marker='o', alpha=0.5) # Outliers

# 4. Estetica "Clean"
ax.set_title('Impatto degli Eventi sui Flussi Turistici', fontsize=16, pad=20, fontweight='bold', color='#333333')
ax.set_ylabel('Numero Totale di Arrivi', fontsize=12, color='#555555')

# Griglia orizzontale
ax.yaxis.grid(True, color='#EEEEEE', linestyle='-')
ax.xaxis.grid(False)
ax.set_axisbelow(True)

# Rimozione bordi
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#CCCCCC')

# Formattazione asse Y con separatore migliaia
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

# 5. Aggiunta Annotazione Informativa
testo_annotazione = (f"Media SENZA Eventi: {int(media_no):,}\n"
                     f"Media CON Eventi: {int(media_si):,}\n"
                     f"Differenza: +{incremento:.1f}%")

# Posizioniamo il testo nel grafico
ax.text(0.05, 0.95, testo_annotazione, transform=ax.transAxes, 
        fontsize=11, verticalalignment='top', 
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='#DDDDDD'))

plt.tight_layout()
plt.show()