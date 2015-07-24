import matplotlib.pyplot as plt
from pymapgb import GBBasemap

fig, ax = plt.subplots(figsize=(8, 12))

GBmap = GBBasemap(ax, threshold=50)

for country in ['england', 'wales', 'scotland']:
    GBmap.draw_by_request("country", country, facecolor="w", edgecolor="k")
    GBmap.draw_by_request("counties", country, colors='random')

GBmap.ax.autoscale()
plt.savefig("counties.png")


