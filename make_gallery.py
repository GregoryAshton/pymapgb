import matplotlib.pyplot as plt
from pymapgb import GBBasemap

# Demo
fig, ax = plt.subplots(figsize=(8, 12))
GBmap = GBBasemap(ax)
GBmap.draw_country(["england", "wales"], color="w", linewidth=2, edgecolor="k")
GBmap.draw_country("scotland", color="w", linewidth=2, edgecolor="k")
GBmap.draw_counties_for_country(["scotland", "wales", "england"])
GBmap.ax.autoscale()
plt.savefig("img/demo.png")

# gb_dictricts
fig, ax = plt.subplots(figsize=(8, 12))
GBmap = GBBasemap(ax, threshold=100)
GBmap.draw_counties_for_country("gb")
GBmap.ax.autoscale()
plt.savefig("img/gb_districs.png")

fig, ax = plt.subplots(figsize=(8, 12))
GBmap = GBBasemap(ax, threshold=300)
GBmap.draw_by_file_name("gb_wpc_2010_05")
GBmap.ax.autoscale()
plt.savefig("img/gb_wpc.png")
 
