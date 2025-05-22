import json
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

# Load the JSON file
file_path = ".BSC3K.json"  # Update this path as needed
with open(file_path, "r") as f:
    json_data = json.load(f)

# Extract the matrix data
raw_values = json_data["data"]["result"][0]["values"]

# Convert to DataFrame
df = pd.DataFrame(raw_values, columns=["timestamp", "value"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
df["value"] = df["value"].astype(float)

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["value"], marker='o', linestyle='-')
plt.title("Temperature Over Time")
plt.xlabel("Timestamp")
plt.ylabel("Temperature (mK)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
