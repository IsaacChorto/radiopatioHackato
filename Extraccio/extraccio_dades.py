import os
import pandas as pd
import glob
import matplotlib.pyplot as plt
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split

# Defineix la ruta relativa a la carpeta Dataset des de Extraccions
dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Dataset")

# Busca tots els fitxers CSV dins de Dataset
fitxers = glob.glob(os.path.join(dataset_path, "*.csv"))

# Llista per guardar les dades
dades_totals = []

# Funció per calcular les mitjanes per franja horària
def calcular_mitjanes(row):
    mati = row[["h07", "h08", "h09", "h10", "h11", "h12"]].mean()
    tarda = row[["h13", "h14", "h15", "h16", "h17", "h18"]].mean()
    nit = row[["h19", "h20", "h21", "h22", "h23", "h24", "h01", "h02", "h03", "h04", "h05", "h06"]].mean()
    return pd.Series([mati, tarda, nit], index=["mitjana_mati", "mitjana_tarda", "mitjana_nit"])

# Processar cada fitxer
for fitxer in fitxers:
    df = pd.read_csv(fitxer)
    
    # Seleccionar columnes necessàries
    df_seleccionat = df[["nom_estacio", "data", "contaminant"] + [f"h{i:02}" for i in range(1, 25)]]
    
    df_seleccionat = df_seleccionat.copy()

    # Convertir unitats de CO de mg/m³ a µg/m³
    df_seleccionat.loc[df_seleccionat["contaminant"] == "co", [f"h{i:02}" for i in range(1, 25)]] *= 1000

    df_seleccionat.loc[:, "data"] = df_seleccionat["data"].str.split("T").str[0]  
    df_seleccionat[["any", "mes", "dia"]] = df_seleccionat["data"].str.split("-", expand=True)

    df_seleccionat.loc[:, "any"] = pd.to_numeric(df_seleccionat["any"], errors="coerce")
    df_seleccionat.loc[:, "mes"] = pd.to_numeric(df_seleccionat["mes"], errors="coerce")
    df_seleccionat.loc[:, "dia"] = pd.to_numeric(df_seleccionat["dia"], errors="coerce")

    # Calcular mitjanes
    df_mitjanes = df_seleccionat.apply(calcular_mitjanes, axis=1)
    
    # Combinar dades finals
    df_final = pd.concat([df_seleccionat[["nom_estacio", "data", "contaminant", "dia", "mes", "any"]], df_mitjanes], axis=1)
    
    # Afegir al conjunt de dades
    dades_totals.append(df_final)

# Concatenar totes les dades
dades_resultants = pd.concat(dades_totals, ignore_index=True)

# Separar per nom d'estació
estacions = dades_resultants["nom_estacio"].unique()

for estacio in estacions:
    print(f"🔹 Processant estació: {estacio}")

    # Filtrar dades per estació
    dades_estacio = dades_resultants[dades_resultants["nom_estacio"] == estacio].copy()

    # Separar per contaminant
    contaminants = dades_estacio["contaminant"].unique()

    prediccions_contaminacio = {}

    for contaminant in contaminants:
        print(f"   ➡ Entrenant model per {contaminant}")

        # Filtrar dades per contaminant
        dades_contaminant = dades_estacio[dades_estacio["contaminant"] == contaminant].copy()

        # Separar features (X) i valors de contaminació (y)
        X = dades_contaminant[["dia", "mes", "any", "mitjana_mati", "mitjana_tarda", "mitjana_nit"]]
        y = dades_contaminant["mitjana_mati"]  # Suposant que volem predir la contaminació matinal

        if len(X) < 10:
            print(f"   ⚠ Poques dades per {contaminant}, es descarta la predicció.")
            continue

        # Dividir les dades en entrenament i test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrenar un model CatBoost per cada contaminant
        # Comprovar si hi ha valors NaN
        if y_train.isna().sum() > 0:
            print(f"   ⚠ {y_train.isna().sum()} valors NaN trobats a {contaminant}. Es descarten aquestes files.")
            X_train = X_train.dropna()
            y_train = y_train[X_train.index]

        # Entrenar el model si queden dades suficients
        if len(X_train) < 10:
            print(f"   ⚠ Poques dades vàlides per {contaminant}, es descarta la predicció.")
            continue

        model = CatBoostRegressor(iterations=500, learning_rate=0.05, depth=6, verbose=100)
        model.fit(X_train, y_train)


        # Fer predicció per una data específica
        dia_prediccio = 14
        mes_prediccio = 8
        any_prediccio = 2025

        entrada = pd.DataFrame([[dia_prediccio, mes_prediccio, any_prediccio, 0, 0, 0]], columns=X.columns)
        prediccio = model.predict(entrada)[0]

        prediccions_contaminacio[contaminant] = prediccio

    # Mostrar resultats
    print(f"📊 Predicció per {estacio} el {dia_prediccio}/{mes_prediccio}/{any_prediccio}:")
    for contaminant, valor in prediccions_contaminacio.items():
        print(f"{contaminant}: {valor:.2f} µg/m³")
