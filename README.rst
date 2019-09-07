Automatic Graph Visualizer (AGVIZ)
==================================

.. figure:: https://github.com/idekerlab/auto-graph-visualizer/blob/master/images/sample_out2.png
   :alt: sample\_output2

   sample\_output

**An automatic graph visualize package for
`Cytoscape <https://cytoscape.org/>`__.**

More Details
------------

Automatic Graph Visualizer[AGVIZ] is one of the Cytoscape Projects.
AGVIZ attaches some visualize information for the Cytoscape to the
network structure information (`CX
format <https://home.ndexbio.org/data-model/>`__).

System Requirements
-------------------

To use AGVIZ, you need the following:

-  Ubuntu (Recommend >=18.04) or macOS (Recommend >=10.14)

   -  **Windows is not supported**

-  Python 3.x

Installing
----------

Download or clone this repository

::

    $ git clone https://github.com/idekerlab/auto-graph-visualizer

In the downloaded (cloned) directory, install using setup.py

::

    $ python3 setup.py install

Known issues in installing
^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Perhaps, you have some error in ``python-igraph`` installation
   depending on some environments. In such case, try the following
   installation before setup.

   ::

       $ apt install build-essential python3-dev libxml2 libxml2-dev zlib1g-dev

   .. rubric:: Usage
      :name: usage

   ::

       $ cat your_file | agviz

   Options:

-  -n : Output graph name (.cx). (default : 'test\_out')
-  -p : Output directory path. (default : './')
-  -a : Community detection algorithm. (default : 'greedy')

   -  greedy : Based on the greedy optimization of modularity
      `detail <https://journals.aps.org/pre/abstract/10.1103/PhysRevE.70.066111>`__
   -  eigenvec : Newman's eigenvector community structure detection.
      `detail <https://journals.aps.org/pre/abstract/10.1103/PhysRevE.74.036104>`__
   -  labelprop : The label propagation method of Raghavan et al.
      `detail <https://journals.aps.org/pre/abstract/10.1103/PhysRevE.76.036106>`__

-  -cp : Base color palette. (default : 'hls')

   -  hls

   -  Accent

   -  Set1

   -  brg

   -  hsv

   -  gnuplot

-  -ns : The standard of nodesize. (default : 'betweenness')

   -  closeness
   -  degree
   -  pagerank
   -  betweenness
   -  diversity

-  -maxns : Value of criterion which maximum the node size. (default :
   1000000 \*you may need adjust this value according to the criterion
   and the network)

-  -d : Density of output graph.(default : 'normal')

   -  density
   -  normal
   -  sparse

-  -pos : Algorithm of node positioning for graph layout.(default :
   'fa')

   -  fa :
      `forceatras2 <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0098679>`__
   -  kk : kamada-kawai >Tomihisa Kamada and Satoru Kawai. An Algorithm
      for Drawing General Undirected Graphs. Information Processing
      Letters 31:7-15, 1989.

Authors
-------

-  **Keiichiro Ono** (`Github <https://github.com/keiono>`__)
-  **Atsuya Matsubara** (`Github <https://github.com/ray0bump0>`__)
-  **Mikio Shiga** (`Github <https://github.com/agis09>`__)

License
-------

This project is licensed under the MIT License - see the
`LICENSE <LICENSE>`__ file for details
