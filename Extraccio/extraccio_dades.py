import os
import pandas as pd
import glob
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

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
    
    df_seleccionat = df_seleccionat.copy()  # Afegir aquesta línia per evitar l'error

    df_seleccionat.loc[:, "data"] = df_seleccionat["data"].str.split("T").str[0]  # Elimina la part de l'hora
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

# Codificar els contaminants a valors numèrics
label_encoder = LabelEncoder()
dades_resultants["contaminant_codificat"] = label_encoder.fit_transform(dades_resultants["contaminant"])

# Separar features (X) i variable objectiu (y)
X = dades_resultants[["dia", "mes", "any", "mitjana_mati", "mitjana_tarda", "mitjana_nit"]]
y = dades_resultants["contaminant_codificat"]

# Dividir les dades en entrenament i test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar un model CatBoost per predir contaminants
model = CatBoostClassifier(iterations=1000, learning_rate=0.05, depth=10, cat_features=[], verbose=100)
model.fit(X_train, y_train)

# Funció per fer la predicció en una data específica
def predir_contaminacio(dia, mes, any):
    entrada = pd.DataFrame([[dia, mes, any, 0, 0, 0]], columns=X.columns)
    probabilitats = model.predict_proba(entrada)[0]
    
    # Obtenir els contaminants predits amb probabilitats
    contaminant_probabilitat = {label_encoder.inverse_transform([i])[0]: probabilitats[i] for i in range(len(probabilitats))}
    
    return contaminant_probabilitat

# Exemple d'ús: predir contaminants pel 10 de febrer de 2025
dia_prediccio = 14
mes_prediccio = 8
any_prediccio = 2025

resultats = predir_contaminacio(dia_prediccio, mes_prediccio, any_prediccio)
print(f"Predicció per {dia_prediccio}/{mes_prediccio}/{any_prediccio}:")
for contaminant, probabilitat in resultats.items():
    print(f"{contaminant}: {probabilitat:.2%}")
