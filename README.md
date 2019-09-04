# Automatic Graph Visualizer (AGVIZ)

An automatic graph visualize package for [Cytoscape](https://cytoscape.org/).

## More Details

Automatic Graph Visualizer[AGVIZ] is one of the Cytoscape Projects. AGVIZ attaches some visualize information for the Cytoscape to the network structure information (CX file). 

## System Requirements

To use AGVIZ, you need the following:

* Ubuntu (Recommend using >=18.04) or macOS (Recommend using >=10.14)
    * **Windows is not supported**
* Python 3.x


## Installing

Download or clone this repository

```
git clone https://github.com/idekerlab/auto-graph-visualizer
```

In the downloaded (cloned) directory, install using setup.py

```
python3 setup.py install
```

#### Known issues in installing
* Perhaps, you have some error in `python-igraph` installation depending on some environments. In such case, try the following installation before setup.
    ```
    apt install build-essential python3-dev libxml2 libxml2-dev zlib1g-dev
    ```
## Usage


## Authors

* **Keiichiro Ono** [Github](https://github.com/keiono)
* **Atsuya Matsubara** [Github](https://github.com/ray0bump0)
* **Mikio Shiga** [Github](https://github.com/agis09)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


