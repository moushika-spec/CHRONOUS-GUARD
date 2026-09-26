import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# STUDENT 1 FEATURE VISUALIZATION
# ============================================================

INPUT_FILE = "output/processed_features.csv"


# Load processed feature data
df = pd.read_csv(INPUT_FILE)


# Create a global sequential index
# This allows us to visualize all processed windows continuously.
df["global_window"] = range(len(df))


print("=" * 50)
print("STUDENT 1 FEATURE VISUALIZATION")
print("=" * 50)

print(f"Total windows: {len(df)}")


# ============================================================
# 1. RMS TREND
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(
    df["global_window"],
    df["rms"]
)

plt.title("RMS Vibration Trend")

plt.xlabel("Processed Window")

plt.ylabel("RMS Amplitude")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "output/rms_trend.png",
    dpi=300
)

plt.show()


# ============================================================
# 2. KURTOSIS TREND
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(
    df["global_window"],
    df["kurtosis"]
)

plt.title("Kurtosis Trend")

plt.xlabel("Processed Window")

plt.ylabel("Kurtosis")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "output/kurtosis_trend.png",
    dpi=300
)

plt.show()


# ============================================================
# 3. RMS Z-SCORE
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(
    df["global_window"],
    df["rms_z_score"]
)

plt.axhline(
    y=3,
    linestyle="--",
    label="Upper Threshold (+3σ)"
)

plt.axhline(
    y=-3,
    linestyle="--",
    label="Lower Threshold (-3σ)"
)

plt.title("RMS Z-Score Deviation")

plt.xlabel("Processed Window")

plt.ylabel("RMS Z-Score")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "output/rms_z_score_trend.png",
    dpi=300
)

plt.show()


# ============================================================
# 4. KURTOSIS Z-SCORE
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(
    df["global_window"],
    df["kurtosis_z_score"]
)

plt.axhline(
    y=3,
    linestyle="--",
    label="Upper Threshold (+3σ)"
)

plt.axhline(
    y=-3,
    linestyle="--",
    label="Lower Threshold (-3σ)"
)

plt.title("Kurtosis Z-Score Deviation")

plt.xlabel("Processed Window")

plt.ylabel("Kurtosis Z-Score")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "output/kurtosis_z_score_trend.png",
    dpi=300
)

plt.show()


print("\nVisualization completed successfully.")

print("\nGenerated plots:")

print("1. output/rms_trend.png")

print("2. output/kurtosis_trend.png")

print("3. output/rms_z_score_trend.png")

print("4. output/kurtosis_z_score_trend.png")