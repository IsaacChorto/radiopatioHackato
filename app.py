from flask import Flask, request, jsonify
import pandas as pd
import os
from Extraccio.extraccio_dades import extraccio_dades  # Assegura't que el mòdul 'extraccio_dades.py' estigui en la mateixa carpeta
from Algoritme.algoritme_reduccio import algorisme_reduccio  # Assegura't que el mòdul 'algoritme_reduccio.py' estigui en la mateixa carpeta

app = Flask(__name__)

# Ruta per executar el codi d'extracció i obtenir les dades
@app.route('/obtenir_prediccions', methods=['GET'])
def obtenir_prediccions():
    # Obtenir paràmetres des del frontend (data i hora)
    dia = request.args.get('dia')
    mes = request.args.get('mes')
    any = request.args.get('any')

    #mostrar la data 
    print(f"📅 Data seleccionada: {dia}/{mes}/{any}")    

    # Executar el procés d'extracció
    extraccio_dades(dia, mes, any)
    

    # Carregar el fitxer CSV amb les prediccions
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Sortida/prediccions_contaminacio.csv")
    
    # Filtrar les dades segons la data i hora seleccionades
    df_prediccions = pd.read_csv(csv_path)
    result = df_prediccions[(df_prediccions['dia'] == int(dia)) & 
                            (df_prediccions['mes'] == int(mes)) & 
                            (df_prediccions['any'] == int(any))]

    fitxer = 'Sortida/prediccions_contaminacio.csv'
    resultats = algorisme_reduccio(fitxer, dia, mes, any)
    #guardar els resultats en un fitxer csv
    resultats.to_csv('Sortida/reduccio_contaminacio.csv', index=False)
    return jsonify(result.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
