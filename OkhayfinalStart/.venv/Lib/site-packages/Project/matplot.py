import matplotlib.pyplot as plt
import numpy as np

# Data
schemes = [
    "TCP Tahoe",
    "TCP Tahoe",
    "TCP Reno",
    "TCP Reno",
    "TCP newReno",
    "TCP newReno",
    "TCP SACK",
    "TCP SACK",
]
queues = ["RED", "DropTail", "RED", "DropTail", "RED", "DropTail", "RED", "DropTail"]
throughputs = [
    802992.69,
    1596350.48,
    1243264.47,
    1596350.48,
    778391.46,
    1596350.48,
    1415959.49,
    1596350.48,
]

# Combine schemes and queues for labels
labels = [f"{scheme}\n({queue})" for scheme, queue in zip(schemes, queues)]

# Plotting
x = np.arange(len(labels))
width = 0.8

plt.figure(figsize=(10, 6))
plt.bar(x, throughputs, color=["#1f77b4" if "RED" in q else "#ff7f0e" for q in queues], width=width)

# Adding labels and title
plt.xlabel("Scheme and Queue", fontsize=12)
plt.ylabel("Average Throughput", fontsize=12)
plt.title("Average Throughput of TCP Variants with Different Queues", fontsize=14)
plt.xticks(x, labels, rotation=45, ha="right", fontsize=10)
plt.tight_layout()

# Adding grid for better visualization
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Display the plot
plt.show()
