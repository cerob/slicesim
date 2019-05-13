import matplotlib.pyplot as plt
from matplotlib import gridspec
import randomcolor
# import numpy as np


class Graph:
    def __init__(self, base_stations, clients):
        self.base_stations = base_stations
        self.clients = clients
        self.fig = plt.figure(figsize=(16,9))
        self.fig.canvas.set_window_title('Network Slicing Simulation')

        self.gs = gridspec.GridSpec(4, 3, width_ratios=[3, 1, 1])

        rand_color = randomcolor.RandomColor()
        colors = rand_color.generate(luminosity='bright', count=len(base_stations))
        # colors = [np.random.randint(256*0.2, 256*0.7+1, size=(3,))/256 for __ in range(len(self.base_stations))]
        for c, bs in zip(colors, self.base_stations):
            bs.color = c
        # TODO prevent similar colors


    def draw_all(self, *stats):
        plt.clf()
        self.draw_map()
        self.draw_stats(*stats)

    def draw_map(self):
        ax = plt.subplot(self.gs[:, 0])
        ax.set_xlim((-1000, 1000))
        ax.set_ylim((-1000, 1000))
        # TODO dynamic xlim, ylim
        ax.set_aspect('equal')
        
        # base stations
        for bs in self.base_stations:
            circle = plt.Circle(bs.coverage.center, bs.coverage.radius,
                                fill=False, linewidth=5, alpha=0.9,
                                color=bs.color)
            ax.add_artist(circle)
        
        # clients
        for c in self.clients:
            # TODO set marker according to size
            ax.scatter(c.x, c.y, color=c.base_station.color if c.base_station is not None else '0.8')
        # ax.plot([c.x for c in self.clients],
        #         [c.y for c in self.clients], '.',
        #         color=c.base_station.color if c.base_station is not None else 'b')

    def draw_stats(self, vals, vals1, vals2, vals3, vals4):
        ax1 = plt.subplot(self.gs[0, 1])
        ax1.plot(vals)
        ax1.set_yticks(range(min(vals), max(vals)+1))
        ax1.set_xlim(left=0)
        ax1.use_sticky_edges = False
        ax1.set_title(f'Total Connected Clients (out of {len(self.clients)} clients)')

        ax2 = plt.subplot(self.gs[1, 1])
        ax2.plot(vals1)
        ax2.set_xlim(left=0)
        ax2.use_sticky_edges = False
        ax2.set_title('Total Bandwidth Usage')

        ax3 = plt.subplot(self.gs[2, 1])
        ax3.plot(vals2)
        ax3.set_xlim(left=0)
        #ax3.set_ylim(0, 1)
        ax3.use_sticky_edges = False
        ax3.set_title('Average Slice Bandwidth Load Ratio')

        ax4 = plt.subplot(self.gs[3, 1])
        ax4.plot(vals3)
        ax4.set_xlim(left=0)
        ax4.use_sticky_edges = False
        ax4.set_title('Average Slice Client Count Ratio')

        ax5 = plt.subplot(self.gs[0, 2])
        ax5.plot(vals4)
        ax5.set_xlim(left=0)
        #ax5.set_ylim(0, 1)
        ax5.use_sticky_edges = False
        ax5.set_title('Coverage Ratio')

        plt.tight_layout()
        # TODO avg client stats

    def save_fig(self):
        self.fig.savefig('base_stations.png', dpi=500) #TODO set dpi

    def show_plot(self):
        plt.show()
