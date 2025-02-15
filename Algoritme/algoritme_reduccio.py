import pandas as pd

def algorisme_reduccio(fitxer: str):
    # Llegir les dades del fitxer prediccions.csv
    df = pd.read_csv(fitxer)

    contaminants_vehicles = ['NOX', 'CO', 'PM10', 'PM2.5', 'NO']
    df_vehicles = df[df['contaminant'].isin(contaminants_vehicles)]

    # Definir les emissions mitjanes per vehicle (en g/km)
    emissions_vehicle = {
        'NOX': 0.3,  
        'CO': 1.5,    
        'PM10': 0.01, 
        'PM2.5': 0.01,
        'NO': 0.2,    
    }

    # Definir les emissions per bus d'emissions baixes (en g/km)
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

    df_vehicles_copy = df_vehicles.copy()
    df_vehicles_copy.loc[:, 'reduccio_contaminacio'] = df_vehicles_copy.apply(calcular_reduccio, axis=1)

    # Guardem també el valor original de la contaminació abans de la reducció
    df_total_reduccio = df_vehicles_copy.groupby('estacio').agg({
        'reduccio_contaminacio': 'sum',
        'prediccio': 'sum'  # Això dona el total original abans de la reducció
    }).reset_index()

    # Canviem el nom per fer-ho més clar
    df_total_reduccio.rename(columns={'prediccio': 'contaminacio_original'}, inplace=True)

    return df_total_reduccio[['estacio', 'contaminacio_original', 'reduccio_contaminacio']]

# Obtenir els resultats
resultats = algorisme_reduccio('Sortida/prediccions_contaminacio.csv')

# Desar els resultats en un fitxer CSV
resultats.to_csv('Sortida/reduccio_contaminacio_per_estacio.csv', index=False)

print("Els resultats s'han desat correctament a 'Sortida/reduccio_contaminacio_per_estacio.csv'.")
