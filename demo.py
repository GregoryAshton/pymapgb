import matplotlib.pyplot as plt
from pymapgb import GBBasemap

fig, ax = plt.subplots(figsize=(8, 12))

GBmap = GBBasemap(ax, clipped=True)
GBmap.draw_country(["england", "wales"], color="w", linewidth=2, edgecolor="k")
GBmap.draw_country("scotland", color="w", linewidth=2, edgecolor="k")
GBmap.draw_counties_for_country(["scotland", "wales", "england"])
GBmap.ax.autoscale()
plt.savefig("demo.png")


