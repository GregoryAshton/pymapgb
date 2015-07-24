import matplotlib.pyplot as plt
from pymapgb import GBBasemap

fig, ax = plt.subplots(figsize=(8, 12))

GBmap = GBBasemap(ax, threshold=50)
GBmap.draw_by_request("country", "england", facecolor="w", edgecolor="k")
GBmap.draw_by_request("country", "wales", facecolor="r", edgecolor="k")
GBmap.draw_by_request("country", "scotland", facecolor="b", lw=2)

GBmap.ax.autoscale()
plt.savefig("countries.png")


