cotwo
=====

(like, carbon dioxide)

Render molecules with Plotly.

Installation
------------

```sh
pip install cotwo
```

or

```sh
uv add cotwo
```

Features
--------

+ Read and display structures from XYZ files
+ Read and display structures from SMILES strings
+ Plot smooth isosurfaces from cube files

![image](https://codeberg.org/crabby/cotwo/raw/branch/main/screenshot.png)

Usage
-----

Use the "Molecule" class to instanciate an object from either an XYZ file (give the path) or a SMILES string:

```py
from cotwo import Molecule

xyz = Molecule.from_xyz("path/to/file.xyz")

smiles = Molecule.from_smiles("CCC(=O)C")
```

To add an isosurface from a density, you need a corresponding `.cube` file.

```py
xyz.add_density("path/to/density.cube", isovalue=0.005, colors=("#909090", "#FF8000"))
```

Then you can either obtain the Plotly `go.Figure`:

```py
fig = xyz.create_fig()
```

or display the plot directly:

```py
xyz.show()
```

Roadmap
-------

Since creating the meshes and the isosurfaces is computationally heavy,
a neat feature would be the possibility to precompute several isosurfaces and keep them in memory.
This way multiple densities can be inspected in short succession without the computational overhead.

In the same vein, it would be cool to load a directory and then be able to select from the available `.cube` files. One could also compute the verticies and faces of the isosurfaces and store
them separately, then loading would be much faster.
That said, it's kind of beyond the scope of this project - best to keep it lightweigth and focused
on only the actual rendering.
