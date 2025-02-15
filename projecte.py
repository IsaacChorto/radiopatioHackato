import os
import sys
import glob
import pandas as pd
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display

# Añadir el directorio padre al path antes de importar graph
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class State(TypedDict):
    name: str
    fitxers: list
    dades_resultants: list

def ingestion_dades(state: State) -> State:
    """
    Ingestión de datos
    """
    dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Dataset")
    fitxers = glob.glob(os.path.join(dataset_path, "*.csv"))
    state["fitxers"] = fitxers
    return state

def calcular_mitjanes(row):
    mati = row[["h07", "h08", "h09", "h10", "h11", "h12"]].mean()
    tarda = row[["h13", "h14", "h15", "h16", "h17", "h18"]].mean()
    nit = row[["h19", "h20", "h21", "h22", "h23", "h24", "h01", "h02", "h03", "h04", "h05", "h06"]].mean()
    return pd.Series([mati, tarda, nit], index=["mitjana_mati", "mitjana_tarda", "mitjana_nit"])

def extraccio_dades(state: State) -> State:
    dades_totals = []
    fitxers = state["fitxers"]
    for fitxer in fitxers:
        df = pd.read_csv(fitxer)
        df_seleccionat = df[["nom_estacio", "data", "magnitud", "contaminant", "unitats"] + 
                            [f"h{i:02}" for i in range(1, 25)]]
        df_mitjanes = df_seleccionat.apply(calcular_mitjanes, axis=1)
        df_final = pd.concat([df_seleccionat[["nom_estacio", "data", "magnitud", "contaminant", "unitats"]], df_mitjanes], axis=1)
        dades_totals.append(df_final)
    
    dades_resultants = pd.concat(dades_totals, ignore_index=True)
    dades_resultants.to_csv("dades_processades.csv", index=False)
    state["dades_resultants"] = dades_resultants
    print("Processament complet. Dades guardades a dades_processades.csv")
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("ingestion_dades", ingestion_dades)

graph_builder.add_node("extraccio_dades", extraccio_dades)

graph_builder.set_entry_point("ingestion_dades")

graph_builder.add_edge("ingestion_dades", "extraccio_dades")

graph_builder.add_edge("extraccio_dades", END)

graph = graph_builder.compile()

graph_image = graph.get_graph().draw_mermaid_png()
with open("graph_visualization.png", "wb") as f:
    f.write(graph_image)

display(Image("graph_visualization.png"))
