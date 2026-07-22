import numpy as np
import pandas as pd
import trimesh
from scipy.spatial import cKDTree
from matplotlib import cm
from matplotlib.colors import Normalize

# =====================================================
# ARQUIVOS
# =====================================================

STL_FILE = "file.stl"
FIELD_FILE = "field.txt"

OUTPUT_PLY = "modelo_colorido.ply"
OUTPUT_OBJ = "modelo_colorido.obj"

# =====================================================
# CARREGA STL
# =====================================================

print("Lendo STL...")

mesh = trimesh.load(STL_FILE, force='mesh')

vertices = mesh.vertices

print(f"Vertices : {len(vertices):,}")
print(f"Faces    : {len(mesh.faces):,}")

# =====================================================
# LÊ O CAMPO DE TENSÃO
# =====================================================

print("Lendo campo de tensões...")

data = pd.read_csv(
    FIELD_FILE,
    sep="\t",
    decimal=",",
    engine="python"
)

# Renomeia para facilitar
data.columns = ["X", "Y", "Z", "Stress"]

data['X'] = data['X']*1/1000
data['Y'] = data['Y']*1/1000
data['Z'] = data['Z']*1/1000

#print(data.head())

coords = data[["X","Y","Z"]].to_numpy(dtype=float)
stress = data["Stress"].to_numpy(dtype=float)

#print(data['Stress'].max(), data['Stress'].min())



print(f"Nós: {len(coords):,}")

# =====================================================
# ATRIBUI TENSÃO AOS VÉRTICES
# =====================================================

print("Criando KDTree...")

tree = cKDTree(coords)

print("Interpolando...")

dist, idx = tree.query(vertices, workers=-1)

vertex_stress = stress[idx]

#print(vertex_stress)

# =====================================================
# COLORAÇÃO
# =====================================================

print("Criando mapa de cores...")

norm = Normalize(
    vmin=vertex_stress.min(),
    vmax=vertex_stress.max()
)


try:
    cmap = cm.get_cmap("jet")
except:
    cmap = cm.get_cmap("viridis")

rgba = cmap(norm(vertex_stress))

mesh.visual.vertex_colors = (rgba*255).astype(np.uint8)

# =====================================================
# EXPORTAÇÃO
# =====================================================

print("Salvando...")

mesh.apply_scale(1000)
mesh.export(OUTPUT_PLY)
mesh.export(OUTPUT_OBJ)

print("\nConcluído!\n")

'''print("Stress mínimo :", vertex_stress.min())
print("Stress máximo :", vertex_stress.max())

print("\nArquivos gerados:")
print(OUTPUT_PLY)
print(OUTPUT_OBJ)

print("Número de índices diferentes:", len(np.unique(idx)))
print("Primeiros 20 índices:", idx[:20])

print("Índice do nó mais usado:", idx[0])
print("Tensão desse nó:", stress[idx[0]])
print("Tensão máxima:", stress.max())

print("Limites STL:")
print(mesh.bounds)

print("\nLimites TXT:")
print(coords.min(axis=0))
print(coords.max(axis=0))'''