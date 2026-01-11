import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# ==============================================================================
# 1. SETUP E FUNZIONI DI UTILITÀ
# ==============================================================================
FILE_PATH = 'data_lucia.csv'

try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print(f"Errore: Il file '{FILE_PATH}' non è stato trovato.")
    exit()

# Funzione per convertire il grafico corrente in stringa Base64 per l'HTML
def get_plot_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close() # Chiude il grafico per liberare memoria
    return img_str

# Stile generale
plt.style.use('default')

# ==============================================================================
# 2. GENERAZIONE DEI GRAFICI
# ==============================================================================

# --- GRAFICO 1: Orizzontale (Top Mesi Evento 0) ---
df_filt = df[df['Evento'] == 0].groupby('Mese')['Arrivi_Stranieri'].sum() / 1000
df_filt = df_filt.sort_values()
colors_1 = ['#D3D3D3'] * len(df_filt)
if len(colors_1) >= 2: colors_1[-1], colors_1[-2] = '#D97C38', '#D97C38'

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.barh(df_filt.index.astype(str), df_filt.values, color=colors_1)
ax1.set_title("Mesi con maggiori Arrivi Stranieri (Senza Eventi)", loc='left', fontsize=14, pad=10)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='x', alpha=0.3)
plot1 = get_plot_base64()

# --- GRAFICO 2: Linee (Confronto Evento 0 vs 1 negli anni) ---
df_pivot = df.pivot_table(index='Anno', columns='Evento', values='Presenze_Stranieri', aggfunc='sum') / 1000
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(df_pivot.index, df_pivot.get(0, []), color='#2F557F', linewidth=2, label='No Evento')
ax2.plot(df_pivot.index, df_pivot.get(1, []), color='#D97C38', linewidth=2, label='Con Evento')
ax2.set_title("Trend Annuale Presenze Stranieri (Migliaia)", fontsize=14, pad=15)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.yaxis.grid(True, color='#EEEEEE')
ax2.legend()
plot2 = get_plot_base64()

# --- GRAFICO 3: Istogramma Mensile (4 Colonne) ---
colonne_y = ['Arrivi_Italiani', 'Arrivi_Stranieri', 'Presenze_Italiani', 'Presenze_Stranieri']
df_grouped = df.groupby('Mese')[colonne_y].sum()
nomi_mesi = {1:'Gen', 2:'Feb', 3:'Mar', 4:'Apr', 5:'Mag', 6:'Giu', 7:'Lug', 8:'Ago', 9:'Set', 10:'Ott', 11:'Nov', 12:'Dic'}
df_grouped.index = df_grouped.index.map(nomi_mesi)
colors_3 = ['#4c72b0', '#dd8452', '#55a868', '#c44e52']

fig3, ax3 = plt.subplots(figsize=(12, 6))
df_grouped.plot(kind='bar', ax=ax3, width=0.85, color=colors_3, edgecolor='white')
ax3.set_title('Confronto Mensile: Arrivi e Presenze Totali', fontsize=14, pad=15)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.yaxis.grid(True, color='#EEEEEE')
plt.xticks(rotation=0)
ax3.legend(ncol=4, frameon=False, loc='upper left')
plot3 = get_plot_base64()

# --- GRAFICO 4: Ciambella (Media Mensile) ---
df['Totale_Arrivi'] = df['Arrivi_Italiani'] + df['Arrivi_Stranieri']
df_pie = df.groupby('Mese')['Totale_Arrivi'].mean()
explode = [0]*12
if not df_pie.empty: explode[df_pie.idxmax()-1] = 0.1
colors_pie = plt.cm.Set3(range(12))

fig4, ax4 = plt.subplots(figsize=(8, 8))
ax4.pie(df_pie, explode=explode, labels=[nomi_mesi[m] for m in df_pie.index], colors=colors_pie, 
        autopct='%1.1f%%', startangle=90, pctdistance=0.85)
ax4.add_artist(plt.Circle((0,0), 0.70, fc='white'))
ax4.set_title('Distribuzione Media Mensile (Totale Arrivi)', fontsize=14)
plot4 = get_plot_base64()

# --- GRAFICO 5: Box Plot (Correlazione Eventi) ---
no_ev = df[df['Evento'] == 0]['Totale_Arrivi']
si_ev = df[df['Evento'] == 1]['Totale_Arrivi']
data_bp = [no_ev, si_ev]

fig5, ax5 = plt.subplots(figsize=(10, 6))
bp = ax5.boxplot(data_bp, patch_artist=True, labels=['No Evento', 'Sì Evento'], showmeans=True, meanline=True)
colors_bp = ['#2F557F', '#D97C38']
for patch, color in zip(bp['boxes'], colors_bp):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax5.set_title('Correlazione: Arrivi Totali con/senza Eventi', fontsize=14, pad=15)
ax5.yaxis.grid(True, color='#EEEEEE')
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)
plot5 = get_plot_base64()

# ==============================================================================
# 3. CREAZIONE FILE HTML
# ==============================================================================

html_content = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Analisi Turismo</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 20px; }}
        .container {{ max_width: 1200px; margin: 0 auto; }}
        h1 {{ text-align: center; color: #2c3e50; margin-bottom: 40px; }}
        .card {{ background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 30px; padding: 20px; }}
        .card h2 {{ font-size: 1.2rem; color: #555; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 0; }}
        .chart-img {{ width: 100%; height: auto; display: block; margin: 0 auto; }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        @media (max-width: 768px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}
        .footer {{ text-align: center; margin-top: 40px; font-size: 0.9rem; color: #777; }}
    </style>
</head>
<body>

<div class="container">
    <h1>📊 Dashboard Analisi Turismo</h1>

    <!-- Riga 1: I due grafici principali -->
    <div class="grid-2">
        <div class="card">
            <h2>Analisi Mesi "No Evento" (Arrivi Stranieri)</h2>
            <img src="data:image/png;base64,{plot1}" class="chart-img">
        </div>
        <div class="card">
            <h2>Trend Annuale Presenze</h2>
            <img src="data:image/png;base64,{plot2}" class="chart-img">
        </div>
    </div>

    <!-- Riga 2: Istogramma grande -->
    <div class="card">
        <h2>Dettaglio Mensile Completo (Arrivi e Presenze)</h2>
        <img src="data:image/png;base64,{plot3}" class="chart-img">
    </div>

    <!-- Riga 3: Torta e Box Plot -->
    <div class="grid-2">
        <div class="card">
            <h2>Distribuzione Stagionale Media</h2>
            <img src="data:image/png;base64,{plot4}" class="chart-img">
        </div>
        <div class="card">
            <h2>Impatto Eventi (Correlazione Statistica)</h2>
            <img src="data:image/png;base64,{plot5}" class="chart-img">
        </div>
    </div>
    
    <div class="footer">
        Generato automaticamente con Python - Dati file: {FILE_PATH}
    </div>
</div>

</body>
</html>
"""

# Scrittura del file
output_file = "dashboard_turismo.html"
with open(output_file, "w", encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Dashboard generata con successo! Apri il file: {output_file}")