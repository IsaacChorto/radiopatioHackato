from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Algorisme de reducció
def algorisme_reduccio(fitxer, dia, mes, any):

    print(f"📅 Data seleccionada: {dia}/{mes}/{any}") 
    # passa les dates a int
    dia = int(dia)
    mes = int(mes)
    any = int(any)   

    
    # Llegir el fitxer sense modificar-lo
    df = pd.read_csv(fitxer)

    contaminants_vehicles = ['NOX', 'CO', 'PM10', 'PM2.5', 'NO']
    # Filtrar per dia, mes i any i contaminant sense modificar el fitxer original
    df_vehicles = df[(df['dia'] == dia) & (df['mes'] == mes) & (df['any'] == any) & (df['contaminant'].isin(contaminants_vehicles))].copy()

    emissions_vehicle = {
        'NOX': 0.3,  
        'CO': 1.5,    
        'PM10': 0.01, 
        'PM2.5': 0.01,
        'NO': 0.2,    
    }

    emissions_bus = {
        'NOX': 0.03,  
        'CO': 0.1,    
        'PM10': 0.001,
        'PM2.5': 0.001,
        'NO': 0.02,
    }

    percentatge_substitucio = 0.10

    def calcular_reduccio(row):
        contaminant = row['contaminant']
        contaminacio_actual = row['prediccio']  # µg/m³

        if contaminant not in emissions_vehicle:
            return 0 

        emission_vehicle = emissions_vehicle[contaminant]
        emission_bus = emissions_bus[contaminant]

        reduccio_per_vehicle = emission_vehicle - emission_bus

        if emission_vehicle == 0:
            return 0

        reduccio_contaminacio = contaminacio_actual * (reduccio_per_vehicle / emission_vehicle) * percentatge_substitucio
        return reduccio_contaminacio

    # Crear una còpia de df_vehicles per no modificar el DataFrame original
    df_vehicles_copy = df_vehicles.copy()
    df_vehicles_copy.loc[:, 'reduccio_contaminacio'] = df_vehicles_copy.apply(calcular_reduccio, axis=1)

    # Resultats agrupats per estació
    df_total_reduccio = df_vehicles_copy.groupby('estacio').agg({
        'reduccio_contaminacio': 'sum',
        'prediccio': 'sum'  
    }).reset_index()

    # Renombrar columna per fer-la més clara
    df_total_reduccio.rename(columns={'prediccio': 'contaminacio_original'}, inplace=True)

    # Seleccionar les columnes finals per als resultats
    resultats = df_total_reduccio[['estacio', 'contaminacio_original', 'reduccio_contaminacio']]

    # Guardar els resultats en un nou fitxer CSV, sense modificar el fitxer original
    resultats.to_csv('Sortida/reduccio_contaminacio.csv', index=False)

    return resultats

# Ruta per obtenir la reducció
if __name__ == '__main__':
    fitxer = 'Sortida/prediccions_contaminacio.csv'
    resultats = algorisme_reduccio(fitxer, 16, 2, 2025)
