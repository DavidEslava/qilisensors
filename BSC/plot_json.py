import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set base data folder
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Store all readings
p5_data, pc_data, mxc_data = [], [], []

# Traverse folders and collect data from each file
for folder in sorted(os.listdir(base_path)):
    folder_path = os.path.join(base_path, folder)
    if not os.path.isdir(folder_path):
        continue

    files = {
        "P5": "directory_monitor_P5.json",
        "PC": "directory_monitor_Pc.json",
        "MXC": "directory_monitor_T4CMN_195_2CMN_195_2.json"
    }

    for key, fname in files.items():
        path = os.path.join(folder_path, fname)
        if os.path.exists(path):
            with open(path, "r") as f:
                try:
                    data = json.load(f)["data"]["result"][0]["values"]
                    for ts, val in data:
                        if key == "P5":
                            p5_data.append((int(ts), float(val)))
                        elif key == "PC":
                            pc_data.append((int(ts), float(val)))
                        elif key == "MXC":
                            mxc_data.append((int(ts), float(val)))
                except Exception as e:
                    print(f"Error reading {path}: {e}")

# Convert to DataFrames
df_p5 = pd.DataFrame(p5_data, columns=["timestamp", "P5_mbar"])
df_pc = pd.DataFrame(pc_data, columns=["timestamp", "PC_mbar"])
df_mxc = pd.DataFrame(mxc_data, columns=["timestamp", "MXC_mK"])

# Merge all on timestamp
df = pd.merge(df_p5, df_pc, on="timestamp", how="outer")
df = pd.merge(df, df_mxc, on="timestamp", how="outer")

# Convert and sort timestamps
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
df = df.sort_values("timestamp").drop_duplicates()

# Plot all metrics
fig, ax1 = plt.subplots(figsize=(14, 6))
ax1.plot(df["timestamp"], df["P5_mbar"], label="P5 Pressure (mbar)", color="orange")
ax1.plot(df["timestamp"], df["PC_mbar"], label="PC Pressure (mbar)", color="blue")
ax1.set_ylabel("Pressure (mbar)")
ax1.set_xlabel("Date and Time")
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True)

# MXC temperature on secondary axis
ax2 = ax1.twinx()
ax2.plot(df["timestamp"], df["MXC_mK"], label="MXC Temperature (mK)", color="green")
ax2.set_ylabel("Temperature (mK)")
ax2.set_ylim(5, 30)  # lock MXC temp axis between 5 and 30 mK

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.title("P5 and PC Pressures with MXC Temperature")
plt.tight_layout()
plt.show()
