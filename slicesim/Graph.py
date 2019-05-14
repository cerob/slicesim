import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import gridspec
import randomcolor


class Graph:
    def __init__(self, base_stations, clients, xlim):
        self.base_stations = base_stations
        self.clients = clients
        self.xlim = xlim
        self.fig = plt.figure(figsize=(16,9))
        self.fig.canvas.set_window_title('Network Slicing Simulation')

        self.gs = gridspec.GridSpec(4, 3, width_ratios=[6, 3, 3])

        rand_color = randomcolor.RandomColor()
        colors = rand_color.generate(luminosity='bright', count=len(base_stations))
        # colors = [np.random.randint(256*0.2, 256*0.7+1, size=(3,))/256 for __ in range(len(self.base_stations))]
        for c, bs in zip(colors, self.base_stations):
            bs.color = c
        # TODO prevent similar colors

    def draw_live(self, *stats):
        ani = animation.FuncAnimation(self.fig, self.draw_all, fargs=stats, interval=1000)
        plt.show()

    def draw_all(self, *stats):
        plt.clf()
        self.draw_map()
        self.draw_stats(*stats)

    def draw_map(self):
        markers = ['o', 's', 'p', 'P', '*', 'H', 'X', 'D', 'v', '^', '<', '>', '1', '2', '3', '4']
        self.ax = plt.subplot(self.gs[:, 0])
        xlims, ylims = self.get_map_limits()
        self.ax.set_xlim(xlims)
        self.ax.set_ylim(ylims)
        self.ax.set_aspect('equal')
        
        # base stations
        for bs in self.base_stations:
            circle = plt.Circle(bs.coverage.center, bs.coverage.radius,
                                fill=False, linewidth=5, alpha=0.9, color=bs.color)
            self.ax.add_artist(circle)
        
        # clients
        legend_indexed = []
        for c in self.clients:
            label = None
            if c.subscribed_slice_index not in legend_indexed and c.base_station is not None:
                label = c.get_slice().name
                legend_indexed.append(c.subscribed_slice_index)
            self.ax.scatter(c.x, c.y,
                            color=c.base_station.color if c.base_station is not None else '0.8',
                            label=label,
                            marker=markers[c.subscribed_slice_index % len(markers)])
        leg = self.ax.legend()

        for i in range(len(legend_indexed)):
            leg.legendHandles[i].set_color('k')

    def draw_stats(self, vals, vals1, vals2, vals3, vals4):
        self.ax1 = plt.subplot(self.gs[0, 1])
        self.ax1.plot(vals)
        self.ax1.set_xlim(self.xlim)
        locs = self.ax1.get_xticks()
        locs[0] = self.xlim[0]
        locs[-1] = self.xlim[1]
        self.ax1.set_xticks(locs)
        self.ax1.use_sticky_edges = False
        self.ax1.set_title(f'Total Connected Clients (out of {len(self.clients)} clients)')

        self.ax2 = plt.subplot(self.gs[1, 1])
        self.ax2.plot(vals1)
        self.ax2.set_xlim(self.xlim)
        self.ax2.set_xticks(locs)
        self.ax2.use_sticky_edges = False
        self.ax2.set_title('Total Bandwidth Usage')

        self.ax3 = plt.subplot(self.gs[2, 1])
        self.ax3.plot(vals2)
        self.ax3.set_xlim(self.xlim)
        self.ax3.set_xticks(locs)
        self.ax3.use_sticky_edges = False
        self.ax3.set_title('Average Slice Bandwidth Load Ratio')

        self.ax4 = plt.subplot(self.gs[3, 1])
        self.ax4.plot(vals3)
        self.ax4.set_xlim(self.xlim)
        self.ax4.set_xticks(locs)
        self.ax4.use_sticky_edges = False
        self.ax4.set_title('Average Slice Client Count Ratio')

        self.ax5 = plt.subplot(self.gs[0, 2])
        self.ax5.plot(vals4)
        self.ax5.set_xlim(self.xlim)
        self.ax5.set_xticks(locs)
        self.ax5.use_sticky_edges = False
        self.ax5.set_title('Coverage Ratio')

        plt.tight_layout()
        # TODO avg client stats

    def save_fig(self):
        self.fig.savefig('base_stations.png', dpi=500) #TODO set dpi

    def show_plot(self):
        plt.show()

    def get_map_limits(self):
        x_min = min([bs.coverage.center[0]-bs.coverage.radius for bs in self.base_stations])
        x_max = max([bs.coverage.center[0]+bs.coverage.radius for bs in self.base_stations])
        y_min = min([bs.coverage.center[1]-bs.coverage.radius for bs in self.base_stations])
        y_max = max([bs.coverage.center[1]+bs.coverage.radius for bs in self.base_stations])

        return (x_min, x_max), (y_min, y_max)
