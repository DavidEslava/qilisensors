import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Automatically get directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data", "BSC3K.json")

# Check if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Load and parse the JSON file
with open(file_path, "r") as f:
    json_data = json.load(f)

raw_values = json_data["data"]["result"][0]["values"]
df = pd.DataFrame(raw_values, columns=["timestamp", "value"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
df["value"] = df["value"].astype(float)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["value"], marker='o', linestyle='-', color='orange')
plt.title("Temperature Over Time")
plt.xlabel("Timestamp")
plt.ylabel("Temperature (mK)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
