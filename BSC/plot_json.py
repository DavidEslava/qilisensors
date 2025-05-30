import json
import os
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# Define base folder
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

all_values = []

# Traverse all timestamped subfolders and collect data
for subfolder in sorted(os.listdir(base_path)):
    subfolder_path = os.path.join(base_path, subfolder)
    if os.path.isdir(subfolder_path):
        target_file = os.path.join(subfolder_path, "directory_monitor_P5.json")
        if os.path.exists(target_file):
            try:
                with open(target_file, "r") as f:
                    data = json.load(f)
                    values = data["data"]["result"][0]["values"]
                    all_values.extend(values)
            except Exception as e:
                print(f"Error reading {target_file}: {e}")

# Check and process
if not all_values:
    raise ValueError("No P5 data found in any folder.")

df = pd.DataFrame(all_values, columns=["timestamp", "value"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
df["value"] = df["value"].astype(float)
df = df.sort_values("timestamp")

# Plotting
plt.figure(figsize=(14, 6))
plt.plot(df["timestamp"], df["value"], marker='o', linestyle='-', color='orange')
plt.title("P5 Pressure Over Time")
plt.xlabel("Date and Time")
plt.ylabel("P5 Pressure (mbar)")
plt.grid(True)

# X-axis ticks every 2 hours
locator = mdates.HourLocator(interval=2)
formatter = mdates.DateFormatter('%m-%d %H:%M')
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
