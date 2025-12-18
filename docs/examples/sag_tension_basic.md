# Sag-Tension Analysis Example

This example shows a complete sag-tension calculation workflow using Ohmly: from
loading a conductor to evaluating multiple mechanical hypotheses.


## 1. Load a conductor

```python
from ohmly import ConductorRepository

repo = ConductorRepository()
conductor = repo.get(legacy_code="LA 280 HAWK")

print(conductor)
```

If you print the conductor, you should see the following output in your terminal

```bash
  Attribute              Unit             Value  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  designation               -   242-AL1/39-ST1A  
  legacy_code               -       LA 280 HAWK  
  al_area                 mm²             241.6  
  steel_area              mm²              39.5  
  total_area              mm²             281.1  
  al_strands                -                26  
  steel_strands             -                 7  
  core_diameter            mm              8.04  
  overall_diameter         mm              21.8  
  mass                  kg/km             976.2  
  rated_strength          daN            8489.0  
  resistance_dc          Ω/km            0.1195  
  elastic_modulus      kN/mm²            7300.0  
  thermal_exp_factor     1/°C          1.89e-05  
  unit_weight           daN/m            0.9573
```


## 2. Create a mechanical analysis context

The mechanical analysis context binds

-   the conductor, and
-   the environmental zone (ITC-LAT 07)

```python
from ohmly import MechAnalysis, MechAnalysisZone

mech = mechanalysis(
    conductor=conductor,
    zone=mechanalysiszone.b,  # 500–1000 m, ice considered
)
```


## 3. Define mechanical hypotheses

Each hypothesis represents a load scenario defined by:

-   temperature,
-   fraction of rated tensile strength (RTS),
-   wind speed, and
-   ice presence.

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

wind = MechAnalysisHypothesis(
    name="Wind",
    temp=-10,
    rts_factor=0.40,
    wind_speed=120,
)

ice = MechAnalysisHypothesis(
    name="Ice",
    temp=-15,
    rts_factor=0.40,
    with_ice=True,
)

hypotheses = [eds, chs, wind, ice]
```


## 4. Define spans and compute sag-tension

```python
spans = [200, 300, 400]  # meters

table = mech.stt(hypotheses, spans)
print(table)
```

You should see the following sag-tension table in your terminal.

```bash
               EDS               CHS              Wind               Ice        
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

## Complete example

```python
from ohmly import ConductorRepository, MechAnalysis, MechAnalysisHypothesis, MechAnalysisZone

repo = ConductorRepository()
conductor = repo.get(legacy_code="LA 280 HAWK")

# Optionally, you can print the conductor's information.
# print(conductor)

mech = mechanalysis(
    conductor=conductor,
    zone=mechanalysiszone.b,  # 500–1000 m, ice considered
)

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

wind = MechAnalysisHypothesis(
    name="Wind",
    temp=-10,
    rts_factor=0.40,
    wind_speed=120,
)

ice = MechAnalysisHypothesis(
    name="Ice",
    temp=-15,
    rts_factor=0.40,
    with_ice=True,
)

hypotheses = [eds, chs, wind, ice]
spans = [200, 300, 400]  # meters

table = mech.stt(hypotheses, spans)

print(table)
```
