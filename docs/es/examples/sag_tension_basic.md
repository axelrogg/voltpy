# Ejemplo de cálculo de tabla de tendidos

Este ejemplo muestra un flujo de trabajo completo de cálculo de tendido
utilizando Ohmly: desde la carga de un conductor hasta la evaluación de
múltiples hipótesis mecánicas.


## 1. Cargar un conductor

```python
from ohmly import ConductorRepository

repo = ConductorRepository()
conductor = repo.get(legacy_code="LA 280 HAWK")

print(conductor)
```

Al imprimir el conductor, deberías ver la siguiente salida en tu terminal:

```bash
  Attribute              Unit             Value  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  designation                -   242-AL1/39-ST1A  
  legacy_code                -       LA 280 HAWK  
  al_area                  mm²             241.6  
  steel_area               mm²              39.5  
  total_area               mm²             281.1  
  al_strands                 -                26  
  steel_strands              -                 7  
  core_diameter             mm              8.04  
  overall_diameter          mm              21.8  
  mass                   kg/km             976.2  
  rated_strength           daN            8489.0  
  resistance_dc           Ω/km            0.1195  
  elastic_modulus       kN/mm²            7300.0  
  thermal_exp_factor      1/°C          1.89e-05  
  unit_weight            daN/m            0.9573
```


## 2. Crear un contexto de análisis mecánico

El contexto de análisis mecánico vincula

-   el conductor y
-   la zona ambiental (según la ITC-LAT 07).

```python
from ohmly import MechAnalysis, MechAnalysisZone

mech = MechAnalysis(
    conductor=conductor,
    zone=MechAnalysisZone.B,  # 500–1000 m, se considera hielo
)
```


## 3. Definir las hipótesis mecánicas

Cada hipótesis representa un escenario de carga definido por

-   temperatura,
-   fracción de la resistencia a la tracción asignada (*RTS*),
-   velocidad del viento,
-   presencia de hielo,

```python
from ohmly import MechAnalysisHypothesis

eds = MechAnalysisHypothesis(
    name="EDS",
    temp=15,
    rts_factor=0.15,
)

chs = MechAnalysisHypothesis(
    name="CHS",
    temp=-10,
    rts_factor=0.20,
)

viento = MechAnalysisHypothesis(
    name="Viento",
    temp=-10,
    rts_factor=0.40,
    wind_speed=120,
)

hielo = MechAnalysisHypothesis(
    name="Hielo",
    temp=-15,
    rts_factor=0.40,
    with_ice=True,
)

hipotesis = [eds, chs, viento, hielo]
```

## 4. Definir vanos y calcular la tabla de tendidos

```python
vanos = [200, 300, 400]  # metros

tabla = mech.stt(hypotheses, vanos)
print(tabla)
```

Deberías ver una tabla de tendidos como la siguiente en tu terminal.

```bash
               EDS               CHS             Viento             Hielo       
          T (daN), RTS      T (daN), RTS      T (daN), RTS      T (daN), RTS    
  Span         (%)               (%)               (%)               (%)        
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
   200     1273.3500,        1574.4966,        2039.8037,        2408.7764,     
             15.0000           18.5475           24.0288           28.3753      
   300     1273.3500,        1415.2515,        1988.6685,        2401.1087,     
             15.0000           16.6716           23.4264           28.2849      
   400     1273.3500,        1353.7002,        1965.2758,        2397.3542,     
             15.0000           15.9465           23.1509           28.2407      

```


## Ejemplo completo

```python
from ohmly import ConductorRepository, MechAnalysis, MechAnalysisHypothesis, MechAnalysisZone

# 1. Cargar el conductor
repo = ConductorRepository()
conductor = repo.get(legacy_code="LA 280 HAWK")

# 2. Configurar el contexto de análisis (Zona B de la ITC-LAT 07)
mech = MechAnalysis(
    conductor=conductor,
    zone=MechAnalysisZone.B,
)

# 3. Definir el conjunto de hipótesis reglamentarias
hipotesis = [
    MechAnalysisHypothesis(name="EDS", temp=15, rts_factor=0.15),
    MechAnalysisHypothesis(name="CHS", temp=-10, rts_factor=0.20),
    MechAnalysisHypothesis(name="Viento", temp=-10, rts_factor=0.40, wind_speed=120),
    MechAnalysisHypothesis(name="Hielo", temp=-15, rts_factor=0.40, with_ice=True),
]

# 4. Definir los vanos y calcular la tabla
vanos = [200, 300, 400]
tabla = mech.stt(hypotheses, vanos)

print(tabla)
```
