import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("ragas_evaluation_report_q100.csv")
df_cut = df.iloc[:, 4:]
df_cut_clean = df_cut.dropna()

p = df_cut_clean["context_precision"]
r = df_cut_clean["context_recall"]
df_cut_clean["context_f1"] = np.where((p + r) == 0, 0, 2*p*r/(p+r))

metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "context_f1"]

data = [df_cut_clean[m].values for m in metrics]

plt.figure(figsize=(10, 5))
vp = plt.violinplot(data, showmeans=True, showmedians=True)

# overlay points (jitter)
for i, m in enumerate(metrics, start=1):
    y = df_cut_clean[m].values
    x = np.random.normal(i, 0.06, size=len(y))
    plt.scatter(x, y, alpha=0.35, s=14)

plt.xticks(range(1, len(metrics) + 1), metrics, rotation=25)
plt.ylim(-0.05, 1.05)
plt.title("Distributions des métriques (violin + points)")
plt.ylabel("Score")
plt.tight_layout()
plt.show()


