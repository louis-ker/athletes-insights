import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sys

import matplotlib.pyplot as plt

# Conversion des temps de laptime en secondes pour faciliter la visualisation
df['total_laptime_sec'] = df['laptime_min'] * 60 + df['laptime_sec'] + df['laptime_thousandth'] / 1000

# Création du graphique
plt.figure(figsize=(10, 6))
plt.barh(df['name'], df['total_laptime_sec'], color='skyblue')
plt.xlabel('Temps de course (secondes)')
plt.title('Performances des athlètes en short-track')
plt.gca().invert_yaxis()  # Inverser l'axe y pour afficher le meilleur temps en haut
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()