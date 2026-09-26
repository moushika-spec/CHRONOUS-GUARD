# type:ignore 
import pandas as pd
import matplotlib.pyplot as plt

from config import OUTPUT_FILE

df = pd.read_csv(OUTPUT_FILE)

df["window"] = range(len(df))


plt.figure(figsize=(12,5))

plt.plot(

    df["window"],

    df["anomaly_score"]

)

plt.title("Anomaly Score")

plt.xlabel("Window")

plt.ylabel("Score")

plt.grid()

plt.savefig("output/anomaly_score.png")

plt.show()



plt.figure(figsize=(12,5))

plt.plot(

    df["window"],

    df["health_index"]

)

plt.title("Health Index")

plt.xlabel("Window")

plt.ylabel("Health")

plt.grid()

plt.savefig("output/health_index.png")

plt.show()



plt.figure(figsize=(12,5))

plt.plot(

    df["window"],

    df["remaining_useful_life"]

)

plt.title("Remaining Useful Life")

plt.xlabel("Window")

plt.ylabel("RUL (%)")

plt.grid()

plt.savefig("output/rul.png")

plt.show()

print("Graphs Generated Successfully.")