import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("athletes_500m_full_noNull_ordered.csv")
# Convert laptime columns to a single time format in seconds for comparison
df['total_time'] = df['laptime_min'] * 60 + df['laptime_sec'] + df['laptime_thousandth'] / 1000

# Group by country and competition category, calculating the best lap time for each group
best_laptimes = df.groupby(['country', 'competition'])['total_time'].min().reset_index()

# Plotting
plt.figure(figsize=(12, 6))
for key, grp in best_laptimes.groupby(['country']):
    plt.plot(grp['competition'], grp['total_time'], marker='o', label=key)

plt.title('Best Lap Times by Country Across Competitions')
plt.xlabel('Competition')
plt.ylabel('Best Lap Time (seconds)')
plt.xticks(rotation=45)
plt.legend(title='Country')
plt.tight_layout()
plt.show()