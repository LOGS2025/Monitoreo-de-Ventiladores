import pandas as pd
import matplotlib.pyplot as plt

df_with = pd.read_csv("thermal_log0WithFan.csv")
df_without = pd.read_csv("thermal_log0WithoutFan.csv")

plt.plot(df_with["gpu_hotspot"].rolling(20).mean(), label = "GPU avg Hotspot With fan")
plt.plot(df_with["ssd_load"].rolling(20).mean(), label = "SSD avg load With fan")
plt.plot(df_with["cpu_max_load"], label = "CPU Load With fan")

plt.plot(df_without["gpu_hotspot"].rolling(20).mean(), label = "GPU avg Hotspot Without fan")
plt.plot(df_without["ssd_load"].rolling(20).mean(), label = "SSD avg load Without fan")
plt.plot(df_without["cpu_max_load"], label = "CPU Load Without fan")

df_with = df_with.set_index("timestamp")
df_without = df_without.set_index("timestamp")

plt.legend()
plt.show()

print("CPU avg load with fan:", df_with["cpu_load"].mean())
print("CPU avg load without fan:", df_without["cpu_load"].mean())
print("CPU max avg load with fan:", df_with["cpu_max_load"].mean())
print("CPU max avg load without fan:", df_without["cpu_max_load"].mean())
print("GPU avg Hotspot with fan:", df_with["gpu_hotspot"].mean())
print("GPU avg Hotspot without fan:", df_without["gpu_hotspot"].mean())