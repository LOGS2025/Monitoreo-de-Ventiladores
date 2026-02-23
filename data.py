import pandas as pd
import matplotlib.pyplot as plt

df_with = pd.read_csv(R"C:\Users\lopez\OneDrive\Desktop\Arduino\ventiladorespyino\thermal_log.1000.True.2026_02_22_11_53_05.csv")
df_without = pd.read_csv(R"C:\Users\lopez\OneDrive\Desktop\Arduino\ventiladorespyino\thermal_log.1000.False.2026_02_22_13_01_22.csv")


plt.legend()
plt.show()

