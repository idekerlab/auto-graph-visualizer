# Automatic Graph Visualizer (AGVIZ)

![sample_output](https://github.com/idekerlab/auto-graph-visualizer/blob/master/images/sample_out.png)


An automatic graph visualize package for [Cytoscape](https://cytoscape.org/).

## More Details

Automatic Graph Visualizer[AGVIZ] is one of the Cytoscape Projects. AGVIZ attaches some visualize information for the Cytoscape to the network structure information ([CX format](https://home.ndexbio.org/data-model/)). 

## System Requirements

To use AGVIZ, you need the following:

* Ubuntu (Recommend >=18.04) or macOS (Recommend >=10.14)
    * **Windows is not supported**
* Python 3.x


## Installing

Download or clone this repository

```
$ git clone https://github.com/idekerlab/auto-graph-visualizer
```

In the downloaded (cloned) directory, install using setup.py

```
$ python3 setup.py install
```

#### Known issues in installing
* Perhaps, you have some error in `python-igraph` installation depending on some environments. In such case, try the following installation before setup.
    ```
    $ apt install build-essential python3-dev libxml2 libxml2-dev zlib1g-dev
    ```
## Usage
```
$ cat your_file | agviz
```
you can chose following parameters:

* -n : output graph name(.cx) (default : 'test_out')
* -p : output directory path (default : './')
* -a : community detection algorithm (default : 'greedy')
    * greedy : based on the greedy optimization of modularity. [detail](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.70.066111)
    * leading : Newman's eigenvector community structure detection. [detail](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.74.036104)
    * label : the label propagation method of Raghavan et al. [detail](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.76.036106)
* -cp : base color palette (default : 'hls')
    * hls
    <img src="https://github.com/idekerlab/auto-graph-visualizer/blob/master/images/sample_out.png" width=50%>

    * Accent
    <img src="https://github.com/idekerlab/auto-graph-visualizer/blob/master/images/sample_out_Accent.png" width=50%>

    * Set1
    <img src="https://github.com/idekerlab/auto-graph-visualizer/blob/master/images/sample_out_Set1.png" width=50%>

    * brg
    <img src="https://github.com/idekerlab/auto-graph-visualizer/blob/master/images/sample_out_brg.png" width=50%>

    * hsv
    <img src="https://github.com/idekerlab/auto-graph-visualizer/blob/master/images/sample_out_hsv.png" width=50%>

    * gnuplot
    <img src="https://github.com/idekerlab/auto-graph-visualizer/blob/master/images/sample_out_gnuplot.png" width=50%>
    

## Authors

* **Keiichiro Ono** ([Github](https://github.com/keiono))
* **Atsuya Matsubara** ([Github](https://github.com/ray0bump0))
* **Mikio Shiga** ([Github](https://github.com/agis09))


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


