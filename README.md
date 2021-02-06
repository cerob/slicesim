# SliceSim: A Simulation Suite for Network Slicing in 5G Networks
**Abdurrahman Dilmaç** (abdurrahman.d _at_ icloud _dot_ com)  
**Muhammed Emin Güre** (memingure _at_ gmail _dot_ com)  
*Project Advisor:* **Prof. Tuna Tuğcu**
***
### Introduction
5G widely defines network slicing concept which aims to provide different and separate dedicated logical networks that can be customized to respective services. All slices under a cloud infrastructure are put together with their different requirements, e.g. bandwidth, latency

The purpose of this project is to provide a simulation suite for a network consisting of base stations and clients that possible scenarios of 5G can fit into and make analysis of different concepts easier.

### Approach
- Discrete event simulation
- Using **Python 3.7, Simpy, Matplotlib, KDTree**
- **YAML** for reading input configurations
- Asynchronous programming
- Definitions:
	- **Clients:** Simulation consumers. Generates consume requests by given distribution parameters.
	- **Slices of Base Stations:** Simulation resources.

### Input

#### Settings
```yaml
settings:
  simulation_time: 100 # in seconds
  num_clients: 100
  limit_closest_base_stations: 5 # how many base stations stored in a client instance
  statistics_params:
    warmup_ratio: 0.05 # statistic collection will start from this point
    cooldown_ratio: 0.05 # statistic collection will end at this point
    # Statistic collection will be in this area of the coordinate system
    x:
      min: 0
      max: 1980
    y:
      min: 0
      max: 1980
  logging: False # saving logs to a file
  log_file: output.txt # name of the log file
  plotting_params:
    plotting: True # plot the statistics after execution
    plot_save: True # save plot as image
    plot_show: False # show plot after execution
    plot_file: output.png # name of the plot image
    plot_file_dpi: 1000 # dots per inch for plot image
    scatter_size: 15
```

#### Slices
```yaml
slices:
  slice_name: # name of the slice
    delay_tolerance: 10
    qos_class: 5
    bandwidth_guaranteed: 0 # in bps
    bandwidth_max: 100000000 # in bps
    client_weight: 0.39 # [0,1] - ratio of the clients subscribed to this slice in the system. All weights for slices must be 1 in total
    threshold: 0 # for dynamic slicing (future work)
    # defines the bit usage pattern for client subscribed to this slice
    usage_pattern:
      distribution: randint # distribution name
      params: # distribution parameters
        - 4000000 # min value for this example
        - 800000000 # max value for this example
  slice_name_2:
  	...
```

#### Base Stations
```yaml
base_stations:
  - x: 182 # in meters
    y: 1414 # in meters
    capacity_bandwidth: 20000000000 # in bps
    coverage: 224 # in meters
    # ratios of the slices in this specific base station
    # must be 1 in total for each base station
    ratios:
      slice_name: 0.20 # [0,1]
      slice_name_2: 0.59 # [0,1]
      ...
  - ...
```

#### Mobility Patterns
```yaml
mobility_patterns:
  mobility_pattern_1:
    distribution: normal # distribution name
    params: # distribution parameters
      - 0 # mean value for this example
      - 7 # standard deviation name for this example
    client_weight: 0.10 # [0,1] - ratio of the clients assigned to this pattern in the system. All weights must be 1 in total
  mobility_pattern_2:
  	...
```

#### Client population
```yaml
clients:
  location: # populates the area with the given distributions
    x:
      distribution: randint
      params:
        - 0
        - 1980
    y:
      distribution: randint
      params:
        - 0
        - 1980
  usage_frequency: # defines the usage generation intervals of clients
    distribution: randint
    params:
      - 0
      - 100000
    divide_scale: 1000000 # scaling factor
```

### Usage
Python 3 is required with required dependencies listed in `requirements.txt` installed. Please do not send us email if you haven't done this.

```bash
python -m slicesim <input-file.yml>
```

### Example Output
![Example output for 5000 client in 3600s](https://github.com/cerob/slicesim/blob/master/examples/output_n5000_t3600.png)

### Conclusion
- Increasing number of clients increases used bandwidth,
and yet the simulation showed that block ratio also
elevates for this specific configurations.

This simulation tool can be used for such scenarios as well:

- Testing the effect of different dynamic slicing algorithms
on block and handover ratios.
- Analyzing various mobility patterns of clients using
different statistical distributions.
- Observing the effect of usage frequency of clients and the
effect of clients those are distributed unequally.
- Various Proof of Concepts like common base stations for
multiple service providers.

### Future Work
- Customizable shapes for base station coverages
- Improvements of the software performance
- Dynamic slicing mechanism
- Generation of more test configurations
- Video output of a running simulation

### References
1. 5GPPP Architecture Working Group. View on 5G Architecture. Version 2.0, December 2017
2. CellMapper - https://www.cellmapper.net (10.05.2019)
3. FatihMunicipalityGeographicInformationSystem-
https://gis.fatih.bel.tr/webgis (13.05.2019)
4. https://venturebeat.com/2018/12/12/decoding-5g-a-cheat-
sheet-for-next-gen-cellular-concepts-and-jargon/ (17.03.2019)
