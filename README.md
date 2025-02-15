# Aplicació de Monitorització de Contaminació Ambiental

Aquesta aplicació web permet visualitzar la contaminació ambiental de la zona de Tarragona i consultar la seva predicció futura. Utilitza un mapa interactiu per mostrar els nivells de contaminació de diferents contaminants en temps real i permet a l'usuari obtenir consells útils per protegir la seva salut. Com tambe la funcio de veure la reduccio de la contaminacio en un dia especific.

## Característiques

1. **Selecció de contaminant:**  
   Permet a l'usuari seleccionar entre diferents tipus de contaminació, com CO, NO, O3, PM10, entre altres.

2. **Mapa interactiu:**  
   Utilitza el sistema de mapes de `Leaflet` per mostrar la ubicació de les estacions de mesura de contaminació i els nivells de contaminació mitjançant un mapa de calor (heatmap).

3. **Predicció de contaminació:**  
   Permet a l'usuari visualitzar la predicció de contaminació per a una data seleccionada. Les dades de contaminació són carregades des d'un arxiu CSV o des d'un servei backend (API).

4. **Consells útils:**  
   L'aplicació ofereix consells sobre com protegir-se de la contaminació, com evitar zones de trànsit dens o portar màscares en dies de contaminació elevada.

5. **Gràfic d'evolució de contaminació:**  
   L'aplicació genera un gràfic de línia interactiu que mostra l'evolució de la contaminació en un dia específic.

## Estructura de l'HTML

L'estructura principal de l'HTML consta de:

- **Controls:**  
   Elements per seleccionar el tipus de contaminació, la data i els botons per visualitzar la contaminació actual i la predicció.

- **Mapa:**  
   Un element on es renderitza el mapa interactiu utilitzant la biblioteca `Leaflet`.

- **Botó de consells:**  
   Un botó per mostrar/ocultar els consells útils.

- **Gràfic d'evolució:**  
   Un gràfic generat per la biblioteca `Plotly` que mostra l'evolució dels nivells de contaminació per hora.

## Descripció de les funcionalitats

### 1. Selecció de contaminant

L'usuari pot seleccionar un contaminant de la llista dels principals contaminants de l'aire, com ara:

- CO
- H2S
- NO
- NO2
- NOX
- O3
- PM1
- PM10
- PM2.5
- SO2

### 2. Visualització del mapa de calor

Un cop seleccionat el contaminant i la data, es genera un mapa de calor que mostra les estacions de mesura i els nivells de contaminació per a la data seleccionada. Els nivells de contaminació s'assignen a colors segons la intensitat de la contaminació, des de blau (baix nivell) fins a vermell (alt nivell).

### 3. Predicció de contaminació

L'aplicació carrega un fitxer CSV amb les dades històriques de contaminació o fa una consulta a un backend amb un model d'entrenament per obtenir la predicció de contaminació en temps real.

### 4. Consells útils

Quan l'usuari fa clic al botó "Consells", s'obre una finestra amb consells per protegir-se de la contaminació, com evitar zones amb trànsit dens o utilitzar màscares.

### 5. Gràfic d'evolució

El gràfic interactiu mostra com evolucionen els nivells de contaminació en un període de temps específic (per exemple, a les 12:00). Aquest gràfic es genera utilitzant la biblioteca `Plotly`.

## Com fer servir l'aplicació

1. **Selecció de contaminant:**  
   Fes clic a la llista desplegable de contaminació i selecciona el tipus de contaminant que vols monitoritzar.

2. **Selecciona una data:**  
   Escull una data per la qual vols veure les dades de contaminació.

3. **Visualitza la contaminació actual:**  
   Prem el botó "Veure Contaminació" per veure els nivells de contaminació de l'aire en temps real.

4. **Visualitza la predicció:**  
   Prem el botó "Mostrar Predicció" per veure la predicció de contaminació per a la data seleccionada.

5. **Consulta consells útils:**  
   Fes clic al botó "Consejos" per veure una llista de recomanacions per protegir-te de la contaminació.

6. **Consulta l'evolució de la contaminació:**  
   El gràfic interactiu mostra l'evolució dels nivells de contaminació a l'hora seleccionada.

## Requisits

- **Leaflet** per al mapa interactiu.
- **Plotly** per a la generació de gràfics.
- **PapaParse** per a la manipulació de fitxers CSV.
- **Backend (API)** per a la predicció de contaminació (opcional).

## Instal·lació

1. Descarrega o clona el repositori.
2. Obre l'arxiu `index.html` en un navegador compatible amb JavaScript.

## Notes

- Les dades de contaminació es carreguen des de fitxers CSV. Assegura't que els fitxers estan disponibles a les rutes especificades.
- Aquesta aplicació pot requerir una connexió a internet per carregar les dades en temps real o per obtenir prediccions des d'un backend.

## Contribucions

Les contribucions són benvingudes. Si tens suggeriments o millores, si us plau, obre un "issue" o envia una "pull request".

---

*Creat per RADIOPATIO.*
