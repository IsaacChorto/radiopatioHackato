import pandas as pd
import os

# Carpeta on estan els fitxers
carpeta = "../Dataset"
fitxers = ["bonavista.csv", "parcdelaciutat.csv", "santsalvador.csv", "universitatlaboral.csv"]

# Franges horàries
def calcular_mitjanes(row):
    mati = row[["h07", "h08", "h09", "h10", "h11", "h12"]].mean()
    tarda = row[["h13", "h14", "h15", "h16", "h17", "h18"]].mean()
    nit = row[["h19", "h20", "h21", "h22", "h23", "h24", "h01", "h02", "h03", "h04", "h05", "h06"]].mean()
    return pd.Series([mati, tarda, nit], index=["mitjana_mati", "mitjana_tarda", "mitjana_nit"])

# Llista per guardar les dades
dades_totals = []

# Processar cada fitxer
for fitxer in fitxers:
    path = os.path.join(carpeta, fitxer)
    df = pd.read_csv(path)
    
    # Seleccionar columnes necessàries
    df_seleccionat = df[["nom_estacio", "data", "magnitud", "contaminant", "unitats"] + 
                         [f"h{i:02}" for i in range(1, 25)]]
    
    # Calcular mitjanes
    df_mitjanes = df_seleccionat.apply(calcular_mitjanes, axis=1)
    
    # Combinar dades
    df_final = pd.concat([df_seleccionat[["nom_estacio", "data", "magnitud", "contaminant", "unitats"]], df_mitjanes], axis=1)
    
    # Afegir al conjunt de dades
    dades_totals.append(df_final)

# Concatenar totes les dades
dades_resultants = pd.concat(dades_totals, ignore_index=True)

# Guardar a un nou CSV
dades_resultants.to_csv("dades_processades.csv", index=False)

print("Processament complet. Dades guardades a dades_processades.csv")
