# STL Stress Mapper

Transfer finite element (FEM) von Mises stress results from a nodal text file to an STL surface mesh and export the model with vertex colors for visualization in software that supports colored meshes.


---

## Input Files

### 1. STL Mesh

The STL file contains only the surface geometry.

Example:

```
model.stl
```

---

### 2. Stress Results

The stress field must be exported as a tab-separated text file containing the following columns:

| Column                              |
| ----------------------------------- |
| X Location (mm)                     |
| Y Location (mm)                     |
| Z Location (mm)                     |
| Equivalent (von-Mises) Stress (MPa) |

Example:

```
X Location (mm)    Y Location (mm)    Z Location (mm)    Equivalent (von-Mises) Stress (MPa)
12.239             615.480            -26.832            207.36
...
```

---

## Requirements

Python 3.10+

Install the dependencies:

```bash
pip install numpy pandas scipy trimesh matplotlib
```

---

## Project Structure

```
.
├── model.stl
├── field.txt
├── stress_mapper.py
├── output_colored.ply
├── output_colored.obj
└── README.md
```

---

## Usage

Update the file paths inside the script:

```python
STL_FILE = "model.stl"
FIELD_FILE = "field.txt"
```

Run:

```bash
python stress_mapper.py
```

The script will create:

```
output_colored.ply
output_colored.obj
```
---

## Color Map

The script currently uses the classic FEA color map:

* Blue → Minimum stress
* Green → Intermediate stress
* Yellow → High stress
* Red → Maximum stress

This can be changed by replacing:

```python
cmap = cm.get_cmap("jet")
```

with any Matplotlib colormap.


---

## Dependencies

* NumPy
* Pandas
* SciPy
* Trimesh
* Matplotlib

---

## License

This project is released under the MIT License.

---

