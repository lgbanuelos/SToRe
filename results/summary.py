import pandas as pd
import numpy as np

tabla = pd.read_excel("results.xlsx")

print("mean ==================================================")
print(tabla.mean())

print("\n\nstd ==================================================")
print(tabla.std())

